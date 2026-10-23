import pytest
from src.quality_gates import validate_asset


def test_valid_asset():
    valid = {
        "asset_id": "asset_01",
        "platform": "LinkedIn",
        "format": "Short video",
        "content_pillar": "P1_WORKFLOW",
        "hook": "Why your podcast workflow is broken in 2026",
        "caption": "Scrubbing video timelines takes hours. Here is the modern CreatorOps solution. #CreatorOps #IncuBrix",
        "cta": "Test with 300 free credits at www.incubrix.com",
        "utm_link": "https://www.incubrix.com/?utm_source=linkedin&utm_medium=short_video&utm_campaign=creator_growth_engine_q4&utm_content=asset_01",
        "final_file_url": "dummy_final.mp4",
        "source_file_url": "dummy_spec.json",
        "source_input": "sample_inputs/anchor.md",
        "tools_used": "IncuBrix Engine",
        "rights_checked": "Yes",
        "ai_label_needed": "No",
        "scheduled_date": "2026-11-02 09:00",
        "status": "Ready",
        "notes": "target_metric=3000_views; hook_tested",
    }
    is_ready, violations = validate_asset(valid, base_dir="")
    assert is_ready is True
    assert len(violations) == 0


def test_banned_phrase_violation():
    invalid = {
        "asset_id": "asset_02",
        "platform": "Instagram",
        "format": "Short video",
        "content_pillar": "P1_WORKFLOW",
        "hook": "Guaranteed viral views with this secret trick to explode your reach",
        "caption": "Get 100k followers overnight using this cheat the system method! #Viral",
        "cta": "Click now",
        "utm_link": "https://www.incubrix.com/?utm_source=instagram&utm_medium=short_video&utm_campaign=creator_growth_engine_q4&utm_content=asset_02",
        "final_file_url": "dummy.mp4",
        "source_file_url": "dummy.json",
        "source_input": "sample.md",
        "tools_used": "Engine",
        "rights_checked": "Yes",
        "ai_label_needed": "No",
        "scheduled_date": "2026-11-03 10:00",
        "status": "Ready",
        "notes": "target_metric=1000",
    }
    is_ready, violations = validate_asset(invalid, base_dir="")
    assert is_ready is False
    assert any("banned hyperbolic claim" in v for v in violations)


def test_invalid_platform_and_utm():
    invalid = {
        "asset_id": "asset_03",
        "platform": "MySpace",  # Invalid
        "format": "Short video",
        "content_pillar": "P1_WORKFLOW",
        "hook": "Valid hook text for video testing",
        "caption": "Valid caption text with hashtags #IncuBrix",
        "cta": "Test at www.incubrix.com",
        "utm_link": "http://randomlink.com",  # Invalid
        "final_file_url": "dummy.mp4",
        "source_file_url": "dummy.json",
        "source_input": "sample.md",
        "tools_used": "Engine",
        "rights_checked": "No",  # Invalid
        "ai_label_needed": "Maybe",  # Invalid
        "scheduled_date": "2026-11-04 10:00",
        "status": "Ready",
        "notes": "no_target_metric_here",  # Invalid
    }
    is_ready, violations = validate_asset(invalid, base_dir="")
    assert is_ready is False
    assert any("Invalid platform" in v for v in violations)
    assert any("Invalid UTM link" in v for v in violations)
    assert any("Rights issue" in v for v in violations)
    assert any("target_metric=" in v for v in violations)
