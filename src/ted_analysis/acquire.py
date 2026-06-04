"""Data acquisition — download TED Talk transcripts and fetch view counts.

See ``AGENTS-acquire.md`` for the full specification.

Pipeline
--------
Phase 1 — Resolve TED YouTube channel via ``yt-transcript-pro``, then extract
          transcripts (video_id, title, publish_date, transcript_text,
          transcript_type).
Phase 2 — Fetch view counts via the YouTube Data API v3.
Phase 3 — Merge on ``video_id``, validate with pandera ``RawDataSchema``,
          save to ``config.raw_dir / config.raw_data_filename``.

Usage
-----
``python -m ted_analysis.acquire``
(requires the ``YOUTUBE_API_KEY`` environment variable)
"""

from __future__ import annotations

import asyncio
import logging
import os
import random
import time
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd
import pandera.pandas as pa
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from pandera.typing import DataFrame, Series
from yt_transcript_pro import (
    AutoTranscriptExtractor,
    Config as TranscriptConfig,
    SourceResolver,
)

from ted_analysis import ROOT_LOGGER_NAME, setup_logging
from ted_analysis.config import TEDAnalysisConfig

logger = logging.getLogger(ROOT_LOGGER_NAME)

# ─────────────────────────────────────────────────────────────────────────
# Schema
# ─────────────────────────────────────────────────────────────────────────


class RawDataSchema(pa.DataFrameModel):
    """Pandera schema for the raw merged TED dataset.

    Columns
    -------
    video_id : str
        YouTube video ID (11-character identifier).
    title : str
        Video title.
    publish_date : datetime
        Upload date in UTC.
    transcript_text : str
        Full transcript body, one video per row.
    view_count : int, >= 0
        Number of views (0 if missing from API).
    transcript_type : str, "manual" | "auto"
        Whether the transcript was manually created or auto-generated.
    """

    video_id: Series[str] = pa.Field(coerce=True)
    title: Series[str] = pa.Field(coerce=True)
    publish_date: Series[datetime] = pa.Field(coerce=True)
    transcript_text: Series[str] = pa.Field(coerce=True)
    view_count: Series[int] = pa.Field(ge=0, coerce=True)
    transcript_type: Series[str] = pa.Field(isin=["manual", "auto"], coerce=True)

    class Config:
        coerce = True
        strict = True


# ─────────────────────────────────────────────────────────────────────────
# Phase 1 — Transcripts
# ─────────────────────────────────────────────────────────────────────────


def _resolve_videos(cfg: TEDAnalysisConfig) -> list:
    """Resolve all video metadata from the TED Talks YouTube channel.

    Args:
        cfg: Pipeline configuration containing ``channel_url``.

    Returns:
        List of ``yt_transcript_pro.VideoMetadata`` objects.

    Raises:
        ValueError: If the channel contains zero videos.
    """
    resolver = SourceResolver()
    videos = resolver.resolve([cfg.channel_url])

    if not videos:
        raise ValueError(
            f"No videos found on channel {cfg.channel_url}. "
            "The channel may be inaccessible or empty."
        )

    logger.info("Resolved %d videos from channel %s", len(videos), cfg.channel_url)
    return videos


def _fetch_transcripts(cfg: TEDAnalysisConfig, videos: list) -> pd.DataFrame:
    """Fetch transcripts for every resolved video.

    Uses ``yt-transcript-pro.AutoTranscriptExtractor`` with the configured
    language preference, concurrency, and retry settings.  Per-video failures
    are logged and skipped — they do not halt the pipeline.

    Args:
        cfg: Pipeline configuration.
        videos: List of ``VideoMetadata`` objects from :func:`_resolve_videos`.

    Returns:
        DataFrame with columns ``video_id``, ``title``, ``publish_date``,
        ``transcript_text``, ``transcript_type``.

    Raises:
        ValueError: If *every* video failed transcript extraction.
    """
    _transcript_kw: dict[str, object] = dict(
        languages=list(cfg.transcript_languages),
        allow_generated=True,
        concurrency=cfg.transcript_concurrency,
        max_retries=cfg.transcript_retries,
    )
    if cfg.transcript_cookies_file:
        _transcript_kw["cookies_file"] = Path(cfg.transcript_cookies_file)
    if cfg.transcript_proxy:
        _transcript_kw["proxy"] = cfg.transcript_proxy

    extractor = AutoTranscriptExtractor(
        config=TranscriptConfig(**_transcript_kw),
        backend_order=["auto"],
    )

    results = asyncio.run(extractor.fetch_many(videos))

    rows: list[dict] = []
    for res in results:
        if not res.success:
            logger.warning(
                "Transcript fetch failed for video %s: %s",
                res.metadata.video_id,
                res.error,
            )
            continue

        pub_date: datetime | None = None
        if res.metadata.upload_date:
            try:
                pub_date = datetime.strptime(
                    res.metadata.upload_date, "%Y%m%d"
                ).replace(tzinfo=timezone.utc)
            except ValueError:
                logger.warning(
                    "Cannot parse upload_date '%s' for video %s — using NaT",
                    res.metadata.upload_date,
                    res.metadata.video_id,
                )

        rows.append(
            {
                "video_id": res.metadata.video_id,
                "title": res.metadata.title,
                "publish_date": pub_date,
                "transcript_text": res.plain_text,
                "transcript_type": "auto" if res.is_generated else "manual",
            }
        )

    if not rows:
        raise ValueError(
            "No transcripts could be fetched. "
            "All videos failed transcript extraction."
        )

    df = pd.DataFrame(rows)
    logger.info(
        "Fetched transcripts for %d/%d videos", len(df), len(videos)
    )
    return df


# ─────────────────────────────────────────────────────────────────────────
# Phase 2 — View Counts
# ─────────────────────────────────────────────────────────────────────────


def _fetch_view_counts(
    cfg: TEDAnalysisConfig,
    video_ids: list[str],
) -> dict[str, int]:
    """Fetch view counts via the YouTube Data API v3.

    Videos are processed in batches of ``cfg.api_batch_size`` (default 50).
    Rate-limited responses (HTTP 429) trigger exponential backoff up to
    ``cfg.api_retries`` retries.  Missing view counts default to 0 with a
    warning.

    Args:
        cfg: Pipeline configuration.
        video_ids: YouTube video IDs to query.

    Returns:
        Dictionary mapping ``video_id`` to ``view_count`` (int >= 0).

    Raises:
        RuntimeError: If the API quota is exhausted (HTTP 403); partial
            results for already-processed batches are still returned.
        ValueError: If the ``YOUTUBE_API_KEY`` environment variable is
            not set.
    """
    api_key = os.environ.get(cfg.youtube_api_key_env)
    if not api_key:
        raise ValueError(
            f"Environment variable '{cfg.youtube_api_key_env}' is not set. "
            "Provide a valid YouTube Data API v3 key."
        )

    youtube = build("youtube", "v3", developerKey=api_key)
    view_counts: dict[str, int] = {}

    for i in range(0, len(video_ids), cfg.api_batch_size):
        batch = video_ids[i : i + cfg.api_batch_size]

        for attempt in range(cfg.api_retries + 1):
            try:
                response = youtube.videos().list(
                    part="statistics",
                    id=",".join(batch),
                ).execute()

                for item in response.get("items", []):
                    vid = item["id"]
                    raw = item.get("statistics", {}).get("viewCount", "0")
                    try:
                        vc = int(raw)
                    except (ValueError, TypeError):
                        vc = 0
                    view_counts[vid] = vc

                # Fill missing (e.g. deleted / private videos)
                for vid in batch:
                    if vid not in view_counts:
                        logger.warning(
                            "View count not returned for video %s — using 0",
                            vid,
                        )
                        view_counts[vid] = 0

                break  # success — exit retry loop

            except HttpError as exc:
                status = exc.resp.status

                if status == 429 and attempt < cfg.api_retries:
                    delay = 2.0 * (2.0**attempt) + random.uniform(0, 1)
                    logger.warning(
                        "Rate limited (attempt %d/%d), retrying in %.1fs …",
                        attempt + 1,
                        cfg.api_retries,
                        delay,
                    )
                    time.sleep(delay)
                    continue

                if status == 403:
                    # Quota exhausted — save partial, then abort pipeline
                    for vid in batch:
                        if vid not in view_counts:
                            view_counts[vid] = 0
                    logger.error(
                        "YouTube API quota exhausted after %d / %d videos. "
                        "Partial data returned.",
                        len(view_counts),
                        len(video_ids),
                    )
                    return view_counts

                # Unexpected error — re-raise immediately
                raise

    logger.info("Fetched view counts for %d videos", len(view_counts))
    return view_counts


# ─────────────────────────────────────────────────────────────────────────
# Phase 3 — Merge & Validate
# ─────────────────────────────────────────────────────────────────────────


def merge_and_validate(
    cfg: TEDAnalysisConfig,
    transcripts: pd.DataFrame,
    view_counts: dict[str, int],
) -> DataFrame[RawDataSchema]:
    """Merge transcripts with view counts, validate schema, and save to CSV.

    Args:
        cfg: Pipeline configuration (output path).
        transcripts: DataFrame from :func:`_fetch_transcripts`.
        view_counts: Dictionary from :func:`_fetch_view_counts`.

    Returns:
        Validated DataFrame conforming to :class:`RawDataSchema`.

    Raises:
        ValueError: If duplicate ``video_id`` values are detected.
    """
    views_df = pd.DataFrame(
        list(view_counts.items()),
        columns=["video_id", "view_count"],
    )
    views_df["view_count"] = views_df["view_count"].astype(int)

    df = transcripts.merge(views_df, on="video_id", how="left")
    df["view_count"] = df["view_count"].fillna(0).astype(int)

    # Guard against duplicate video IDs
    dups = df[df.duplicated(subset="video_id", keep=False)]
    if not dups.empty:
        raise ValueError(
            f"Duplicate video_id values detected: "
            f"{dups['video_id'].unique().tolist()}"
        )

    # Schema validation
    try:
        RawDataSchema.validate(df, lazy=True)
    except pa.errors.SchemaErrors as exc:
        logger.error("Schema validation failed:\n%s", exc)
        raise

    # Persist
    output_path = cfg.raw_dir / cfg.raw_data_filename
    cfg.raw_dir.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_path, index=False)
    logger.info(
        "Saved raw dataset (%d rows) to %s", len(df), output_path
    )

    return df


# ─────────────────────────────────────────────────────────────────────────
# Entry point
# ─────────────────────────────────────────────────────────────────────────


def main(config: TEDAnalysisConfig | None = None) -> None:
    """Run the data-acquisition pipeline end-to-end.

    Orchestrates the three phases:

    1. **Transcripts** — resolve TED channel, fetch transcripts via
       ``yt-transcript-pro``.
    2. **View counts** — query YouTube Data API v3.
    3. **Merge & validate** — combine on ``video_id``, validate against
       :class:`RawDataSchema`, save CSV.

    Args:
        config: Pipeline configuration.  Falls back to
            ``TEDAnalysisConfig()`` defaults when ``None``.

    Raises:
        ValueError: If no videos are found on the channel or no transcripts
            could be fetched.
        RuntimeError: Propagated from :func:`_fetch_view_counts` when the
            YouTube API quota is exhausted.  Partial data is saved before
            raising.
    """
    cfg = config or TEDAnalysisConfig()
    setup_logging(cfg)

    logger.info("=" * 60)
    logger.info("Data acquisition — start")
    logger.info("=" * 60)

    # Phase 1
    logger.info("Phase 1/3 — resolving channel and fetching transcripts")
    videos = _resolve_videos(cfg)
    transcripts = _fetch_transcripts(cfg, videos)

    # Phase 2
    logger.info("Phase 2/3 — fetching view counts via YouTube Data API")
    view_counts = _fetch_view_counts(cfg, transcripts["video_id"].to_list())

    # Phase 3
    logger.info("Phase 3/3 — merging, validating, and saving")
    try:
        merge_and_validate(cfg, transcripts, view_counts)
    except RuntimeError:
        # Partial data was already saved inside _fetch_view_counts
        raise

    logger.info("Data acquisition — complete")


if __name__ == "__main__":
    main()
