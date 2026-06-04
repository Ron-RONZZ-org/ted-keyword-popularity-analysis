"""Tests for the data-acquisition module (``acquire.py``).

All tests use synthetic data and mock external services — no network calls.
"""

from __future__ import annotations

from unittest.mock import MagicMock, patch

import pandas as pd
import pandera.pandas as pa
import pytest
from googleapiclient.errors import HttpError

from ted_analysis.acquire import (
    RawDataSchema,
    _fetch_view_counts,
    merge_and_validate,
)
from ted_analysis.config import TEDAnalysisConfig


# ── Helpers ──────────────────────────────────────────────────────────────


def _make_cfg(**overrides: object) -> TEDAnalysisConfig:
    """Create a config with sensible test defaults."""
    params: dict[str, object] = {
        "youtube_api_key_env": "TEST_YOUTUBE_API_KEY",
    } | overrides
    return TEDAnalysisConfig(**params)  # type: ignore[arg-type]


def _youtube_api_response(video_id: str, view_count: int = 5000) -> dict:
    """Simulate a YouTube Data API ``videos.list`` response item."""
    return {
        "id": video_id,
        "statistics": {"viewCount": str(view_count)},
    }


# ── Schema tests ─────────────────────────────────────────────────────────


class TestRawDataSchema:
    """Verify the pandera schema rejects invalid data."""

    @staticmethod
    def _valid_df() -> pd.DataFrame:
        return pd.DataFrame(
            {
                "video_id": ["abc123defgh"],
                "title": ["Test Talk"],
                "publish_date": [pd.Timestamp("2024-01-15", tz="UTC")],
                "transcript_text": ["Some transcript content."],
                "view_count": [5000],
                "transcript_type": ["manual"],
            }
        )

    def test_valid_data_passes(self) -> None:
        """Schema accepts a well-formed row."""
        df = self._valid_df()
        RawDataSchema.validate(df)

    def test_negative_view_count_fails(self) -> None:
        """``view_count`` must be >= 0."""
        df = self._valid_df()
        df["view_count"] = [-1]
        with pytest.raises(Exception, match="view_count"):
            RawDataSchema.validate(df, lazy=True)

    def test_invalid_transcript_type_fails(self) -> None:
        """``transcript_type`` must be 'manual' or 'auto'."""
        df = self._valid_df()
        df["transcript_type"] = ["synthetic"]
        with pytest.raises(Exception, match="transcript_type"):
            RawDataSchema.validate(df, lazy=True)

    def test_missing_column_fails(self) -> None:
        """Schema rejects a DataFrame with missing columns."""
        df = self._valid_df().drop(columns=["view_count"])
        with pytest.raises(Exception, match="view_count"):
            RawDataSchema.validate(df, lazy=True)


# ── View-count fetching (Phase 2) ────────────────────────────────────────


class TestFetchViewCounts:
    """Tests for ``_fetch_view_counts`` with mocked YouTube API."""

    def test_happy_path(self) -> None:
        """All video IDs return view counts correctly."""
        cfg = _make_cfg()
        video_ids = ["vid001", "vid002"]
        api_response = {
            "items": [
                _youtube_api_response("vid001", 1000),
                _youtube_api_response("vid002", 2000),
            ]
        }

        with (
            patch.dict("os.environ", {"TEST_YOUTUBE_API_KEY": "fake-key"}),
            patch(
                "ted_analysis.acquire.build",
                return_value=_mock_youtube(api_response),
            ) as mock_build,
        ):
            result = _fetch_view_counts(cfg, video_ids)

        assert result == {"vid001": 1000, "vid002": 2000}
        mock_build.assert_called_once_with(
            "youtube", "v3", developerKey="fake-key"
        )

    def test_missing_api_key_raises(self) -> None:
        """Missing env var raises ``ValueError`` immediately."""
        cfg = _make_cfg()
        with (
            patch.dict("os.environ", {}, clear=True),
            pytest.raises(ValueError, match="TEST_YOUTUBE_API_KEY"),
        ):
            _fetch_view_counts(cfg, ["vid001"])

    def test_missing_view_count_defaults_to_zero(self) -> None:
        """Videos absent from the API response get view_count 0 with warning."""
        cfg = _make_cfg()
        video_ids = ["vid001", "vid002"]
        api_response = {
            "items": [_youtube_api_response("vid001", 1000)]
        }  # vid002 missing

        with (
            patch.dict("os.environ", {"TEST_YOUTUBE_API_KEY": "fake-key"}),
            patch(
                "ted_analysis.acquire.build",
                return_value=_mock_youtube(api_response),
            ),
        ):
            result = _fetch_view_counts(cfg, video_ids)

        assert result == {"vid001": 1000, "vid002": 0}

    def test_rate_limit_triggers_backoff(self) -> None:
        """HTTP 429 triggers retries; eventually succeeds."""
        cfg = _make_cfg(api_retries=3)
        video_ids = ["vid001"]
        api_response = {"items": [_youtube_api_response("vid001", 500)]}

        # First two calls fail with 429, third succeeds
        mock_youtube = _mock_youtube(
            api_response, fail_status=429, fail_count=2
        )

        with (
            patch.dict("os.environ", {"TEST_YOUTUBE_API_KEY": "fake-key"}),
            patch("ted_analysis.acquire.build", return_value=mock_youtube),
            patch("ted_analysis.acquire.time.sleep"),  # no real waiting
        ):
            result = _fetch_view_counts(cfg, video_ids)

        assert result == {"vid001": 500}

    def test_quota_exhausted_returns_partial(self) -> None:
        """HTTP 403 returns partial data (previous batch results)."""
        cfg = _make_cfg()
        video_ids = ["vid001", "vid002", "vid003"]
        api_response = {
            "items": [
                _youtube_api_response("vid001", 100),
                _youtube_api_response("vid002", 200),
            ]
        }

        # First call succeeds, second call raises 403
        class _Raiser:
            def execute(self) -> dict:
                resp = MagicMock()
                resp.status = 403
                raise HttpError(resp, b"quota")

        youtube_mock = MagicMock()
        youtube_mock.videos.return_value.list.return_value.execute.side_effect = [
            api_response,  # first batch succeeds
            _Raiser(),  # second batch hits quota
        ]

        with (
            patch.dict("os.environ", {"TEST_YOUTUBE_API_KEY": "fake-key"}),
            patch("ted_analysis.acquire.build", return_value=youtube_mock),
        ):
            # Does NOT raise; returns partial
            result = _fetch_view_counts(cfg, video_ids)

        assert result == {"vid001": 100, "vid002": 200, "vid003": 0}

    def test_unexpected_http_error_raises(self) -> None:
        """Non-429/403 errors propagate immediately."""
        cfg = _make_cfg()
        video_ids = ["vid001"]

        resp = MagicMock()
        resp.status = 500
        api_error = HttpError(resp, b"internal error")

        mock_list = MagicMock()
        mock_list.execute.side_effect = api_error

        youtube_mock = MagicMock()
        youtube_mock.videos.return_value.list.return_value = mock_list

        with (
            patch.dict("os.environ", {"TEST_YOUTUBE_API_KEY": "fake-key"}),
            patch("ted_analysis.acquire.build", return_value=youtube_mock),
            pytest.raises(HttpError),
        ):
            _fetch_view_counts(cfg, video_ids)


# ── Merge & Validate (Phase 3) ──────────────────────────────────────────


class TestMergeAndValidate:
    """Tests for ``merge_and_validate`` with synthetic data."""

    def test_happy_path(self) -> None:
        """Merged valid data passes validation and is saved."""
        cfg = _make_cfg()
        transcripts = pd.DataFrame(
            {
                "video_id": ["v1", "v2"],
                "title": ["Talk A", "Talk B"],
                "publish_date": [
                    pd.Timestamp("2024-01-01", tz="UTC"),
                    pd.Timestamp("2024-06-15", tz="UTC"),
                ],
                "transcript_text": ["Transcript A.", "Transcript B."],
                "transcript_type": ["manual", "auto"],
            }
        )
        view_counts = {"v1": 1000, "v2": 2000}

        with patch("ted_analysis.acquire.pd.DataFrame.to_csv") as mock_save:
            result = merge_and_validate(cfg, transcripts, view_counts)

        assert len(result) == 2
        assert list(result["view_count"]) == [1000, 2000]
        mock_save.assert_called_once()

    def test_missing_view_count_filled_with_zero(self) -> None:
        """Videos without view count get 0."""
        cfg = _make_cfg()
        transcripts = pd.DataFrame(
            {
                "video_id": ["v1"],
                "title": ["Talk A"],
                "publish_date": [pd.Timestamp("2024-01-01", tz="UTC")],
                "transcript_text": ["Transcript A."],
                "transcript_type": ["manual"],
            }
        )
        view_counts: dict[str, int] = {}  # no view counts at all

        with patch("ted_analysis.acquire.pd.DataFrame.to_csv"):
            result = merge_and_validate(cfg, transcripts, view_counts)

        assert result["view_count"].iloc[0] == 0

    def test_duplicate_video_id_raises(self) -> None:
        """Duplicate ``video_id`` values raise ``ValueError``."""
        cfg = _make_cfg()
        duplicates = pd.DataFrame(
            {
                "video_id": ["v1", "v1"],
                "title": ["Talk A", "Talk A dup"],
                "publish_date": [
                    pd.Timestamp("2024-01-01", tz="UTC"),
                    pd.Timestamp("2024-01-01", tz="UTC"),
                ],
                "transcript_text": ["Transcript A.", "Transcript A."],
                "transcript_type": ["manual", "manual"],
            }
        )

        with pytest.raises(ValueError, match="Duplicate video_id"):
            merge_and_validate(cfg, duplicates, {"v1": 1000})


# ── Mock helper ──────────────────────────────────────────────────────────


def _mock_youtube(
    api_response: dict,
    fail_status: int | None = None,
    fail_count: int = 0,
):
    """Create a mock YouTube API service that optionally fails N times."""
    youtube_mock = MagicMock()
    execute_call = MagicMock()

    if fail_status is not None and fail_count > 0:
        # Return fail_status for first fail_count calls, then real response
        failures = [_http_error(fail_status) for _ in range(fail_count)]
        execute_call.side_effect = failures + [api_response]
    else:
        execute_call.return_value = api_response

    list_call = MagicMock()
    list_call.execute = execute_call

    videos_mock = MagicMock()
    videos_mock.list.return_value = list_call

    youtube_mock.videos.return_value = videos_mock
    return youtube_mock


def _http_error(status: int) -> HttpError:
    """Build an ``HttpError`` with the given status code."""
    resp = MagicMock()
    resp.status = status
    return HttpError(resp, b"simulated error")
