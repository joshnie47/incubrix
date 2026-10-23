import os
import pytest
from src.dedup import DedupStore, compute_content_hash, normalize_text


def test_normalize_text():
    raw = "  Hello, WORLD!! This is a TEST...  "
    norm = normalize_text(raw)
    assert norm == "hello world this is a test"


def test_compute_content_hash():
    t1 = "Unique content text 123"
    t2 = "Unique content text 123"
    t3 = "Different text"
    assert compute_content_hash(t1) == compute_content_hash(t2)
    assert compute_content_hash(t1) != compute_content_hash(t3)


def test_dedup_store_exact_and_hook(tmp_path):
    db_path = str(tmp_path / "test_store.db")
    store = DedupStore(db_path=db_path)

    # Record first asset
    assert store.record_asset("asset_01", "Full caption text about workflow", "How to save 5 hours", "LinkedIn")

    # Check exact content match
    is_dup, reason = store.check_duplicate("Full caption text about workflow", "Different hook")
    assert is_dup is True
    assert "Exact content match" in reason

    # Check exact hook match
    is_dup, reason = store.check_duplicate("Completely new caption", "How to save 5 hours")
    assert is_dup is True
    assert "Identical hook text" in reason

    # Check brand new asset
    is_dup, reason = store.check_duplicate("Unique new post text", "A brand new hook")
    assert is_dup is False
