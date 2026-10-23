"""
IncuBrix Engine — Run Report & Cost Projection Module
Generates structured run_report.json documenting:
- Input size, items produced, items rejected, duplicates removed
- Runtime in minutes, direct costs, token usage
- 10x and 100x scale cost & runtime projections
Directly feeds Workbook Tab 03_ENGINE_LAUNCH (Rows 18-21).
"""

import json
import os
import time
from typing import Dict, Optional


def generate_run_report(
    run_type: str,
    input_file: str,
    items_produced: int,
    items_rejected: int,
    duplicates_removed: int,
    start_time: float,
    end_time: float,
    output_path: str,
    log_path: str = "",
    direct_cost_usd: float = 0.0,
    status: str = "SUCCESS",
    error_message: Optional[str] = None,
) -> Dict:
    """Generate and write run_report.json."""
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    duration_minutes = round((end_time - start_time) / 60.0, 2)
    if duration_minutes <= 0:
        duration_minutes = 0.08  # ~5 seconds minimum

    # Calculate input size
    input_size_chars = 0
    input_size_words = 0
    if os.path.exists(input_file):
        with open(input_file, "r", encoding="utf-8") as f:
            content = f.read()
            input_size_chars = len(content)
            input_size_words = len(content.split())

    tokens_estimated = input_size_words * 4 + items_produced * 850

    # 10x and 100x Projections
    scale_10x = {
        "input_volume_items": items_produced * 10,
        "estimated_runtime_minutes": round(duration_minutes * 8.5, 1),
        "estimated_cost_usd": round(direct_cost_usd * 10 + 0.45, 2),
    }
    scale_100x = {
        "input_volume_items": items_produced * 100,
        "estimated_runtime_minutes": round(duration_minutes * 75.0, 1),
        "estimated_cost_usd": round(direct_cost_usd * 100 + 4.50, 2),
    }

    report_data = {
        "run_type": run_type,
        "status": status,
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "input_file": input_file,
        "input_size_chars": input_size_chars,
        "input_size_words": input_size_words,
        "items_produced": items_produced,
        "items_rejected": items_rejected,
        "duplicates_removed": duplicates_removed,
        "runtime_minutes": duration_minutes,
        "direct_cost_usd": direct_cost_usd,
        "tokens_estimated": tokens_estimated,
        "scale_projections": {
            "at_10x": scale_10x,
            "at_100x": scale_100x,
        },
        "log_path": log_path,
        "error_message": error_message,
    }

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(report_data, f, indent=2)

    return report_data
