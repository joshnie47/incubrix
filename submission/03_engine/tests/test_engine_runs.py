import os
import tempfile
import pytest
from src.engine import run_engine
from src.exporter import COLUMNS_23


def test_calendar_columns_match_23():
    assert len(COLUMNS_23) == 23
    assert COLUMNS_23[0] == "asset_id"
    assert COLUMNS_23[21] == "duplicate_check"
    assert COLUMNS_23[22] == "completeness_check"


def test_normal_and_repeat_run_simulation():
    with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as tmpdir:
        input_file = "submission/03_engine/sample_inputs/anchor_podcast_episode.md"
        test_db = os.path.join(tmpdir, "test_engine_state.db")
        # Use isolated dedup store in tmpdir so tests do not pollute production state
        report_normal = run_engine(
            command="run",
            input_file=input_file,
            output_dir=tmpdir,
            custom_report_name="test_normal_report.json",
            custom_log_name="test_normal.log",
            dedup_db_path=test_db,
        )
        assert report_normal["items_produced"] == 30
        assert report_normal["status"] == "SUCCESS"
        assert os.path.exists(os.path.join(tmpdir, "calendar.csv"))

        # Test repeat run
        report_repeat = run_engine(
            command="repeat",
            input_file=input_file,
            output_dir=tmpdir,
            custom_report_name="test_repeat_report.json",
            custom_log_name="test_repeat.log",
            dedup_db_path=test_db,
        )
        assert report_repeat["items_produced"] == 0
        assert report_repeat["duplicates_removed"] == 30
        assert report_repeat["status"] == "SUCCESS"
