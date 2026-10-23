"""
IncuBrix Engine — Exporter Module
Exports assets to:
1. calendar.csv (Exactly matching the 23 workbook columns in exact order)
   Computes duplicate_check and completeness_check identically to workbook formulas.
2. scheduler_export.csv (Generic social media scheduler ready for Buffer/Hootsuite/Meta/LinkedIn)
"""

import csv
import os
from typing import Dict, List

COLUMNS_23 = [
    "asset_id",
    "platform",
    "format",
    "content_pillar",
    "hook",
    "caption",
    "cta",
    "utm_link",
    "final_file_url",
    "source_file_url",
    "source_input",
    "tools_used",
    "rights_checked",
    "ai_label_needed",
    "scheduled_date",
    "test_published_url",
    "impressions_or_views",
    "engagement_rate",
    "clicks",
    "status",
    "notes",
    "duplicate_check",
    "completeness_check",
]


def compute_duplicate_check(asset_id: str, all_asset_ids: List[str]) -> str:
    """Mirrors Excel formula: =IF(A5="","",IF(COUNTIF($A$5:$A$154,A5)>1,"DUPLICATE","UNIQUE"))"""
    if not asset_id:
        return ""
    count = all_asset_ids.count(asset_id)
    return "DUPLICATE" if count > 1 else "UNIQUE"


def compute_completeness_check(asset: Dict) -> str:
    """
    Mirrors Excel formula:
    =IF(A5="","",IF(T5="Rejected","REJECTED",IF(AND(B5<>"",C5<>"",D5<>"",E5<>"",F5<>"",G5<>"",H5<>"",I5<>"",J5<>"",M5<>"",O5<>"",T5<>""),"COMPLETE","MISSING FIELDS")))
    Requires: B (platform), C (format), D (content_pillar), E (hook), F (caption), G (cta),
              H (utm_link), I (final_file_url), J (source_file_url), M (rights_checked),
              O (scheduled_date), T (status)
    """
    if not asset.get("asset_id"):
        return ""
    if asset.get("status") == "Rejected":
        return "REJECTED"

    required_keys = [
        "platform",
        "format",
        "content_pillar",
        "hook",
        "caption",
        "cta",
        "utm_link",
        "final_file_url",
        "source_file_url",
        "rights_checked",
        "scheduled_date",
        "status",
    ]

    for key in required_keys:
        val = asset.get(key)
        if val is None or str(val).strip() == "":
            return "MISSING FIELDS"

    return "COMPLETE"


def export_calendar_csv(assets: List[Dict], output_csv_path: str) -> None:
    """Export calendar.csv matching the 23 workbook columns."""
    os.makedirs(os.path.dirname(output_csv_path), exist_ok=True)
    all_ids = [a.get("asset_id", "") for a in assets]

    with open(output_csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(COLUMNS_23)

        for asset in assets:
            a_id = asset.get("asset_id", "")
            dup = compute_duplicate_check(a_id, all_ids)
            comp = compute_completeness_check(asset)

            row = [
                asset.get("asset_id", ""),
                asset.get("platform", ""),
                asset.get("format", ""),
                asset.get("content_pillar", ""),
                asset.get("hook", ""),
                asset.get("caption", ""),
                asset.get("cta", ""),
                asset.get("utm_link", ""),
                asset.get("final_file_url", ""),
                asset.get("source_file_url", ""),
                asset.get("source_input", ""),
                asset.get("tools_used", ""),
                asset.get("rights_checked", ""),
                asset.get("ai_label_needed", ""),
                asset.get("scheduled_date", ""),
                asset.get("test_published_url", ""),
                asset.get("impressions_or_views", ""),
                asset.get("engagement_rate", ""),
                asset.get("clicks", ""),
                asset.get("status", ""),
                asset.get("notes", ""),
                dup,
                comp,
            ]
            writer.writerow(row)


def export_scheduler_csv(assets: List[Dict], output_csv_path: str) -> None:
    """Export generic social media scheduler CSV."""
    os.makedirs(os.path.dirname(output_csv_path), exist_ok=True)
    headers = ["platform", "publish_datetime", "caption", "media_path", "link"]

    with open(output_csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(headers)

        for asset in assets:
            if asset.get("status") == "Ready":
                writer.writerow(
                    [
                        asset.get("platform", ""),
                        asset.get("scheduled_date", ""),
                        f"{asset.get('hook', '')}\n\n{asset.get('caption', '')}\n\n{asset.get('cta', '')}",
                        asset.get("final_file_url", ""),
                        asset.get("utm_link", ""),
                    ]
                )
