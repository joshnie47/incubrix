"""
IncuBrix Engine — Quality Gates & Ready Checks Module
Maps strictly to Section 3 & 6 of the assessment specification.
An asset counts as 'Ready' only when it passes EVERY quality check below.
"""

import os
import re
from typing import Dict, List, Tuple

ALLOWED_PLATFORMS = [
    "LinkedIn",
    "Instagram",
    "YouTube Shorts",
    "TikTok",
    "X",
    "Threads",
    "Facebook",
    "Reddit",
]

ALLOWED_FORMATS = [
    "Short video",
    "Carousel",
    "Graphic",
    "Text post",
    "Thread",
    "Long video",
]

BANNED_PHRASES = [
    "guaranteed viral",
    "100k followers overnight",
    "hack the algorithm",
    "get rich quick",
    "cheat the system",
    "secret trick to explode",
]

REQUIRED_FIELDS = [
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
    "status",
    "notes",
]


def validate_asset(asset: Dict, base_dir: str = "") -> Tuple[bool, List[str]]:
    """
    Validate a single asset dictionary against all 8 quality gates.
    Returns (is_ready: bool, violations: List[str]).
    """
    violations = []

    # 1. Field completeness check
    for field in REQUIRED_FIELDS:
        val = asset.get(field)
        if val is None or str(val).strip() == "":
            violations.append(f"Missing required field: '{field}'")

    # 2. Platform dropdown check
    platform = asset.get("platform", "")
    if platform not in ALLOWED_PLATFORMS:
        violations.append(f"Invalid platform '{platform}'. Must be one of: {ALLOWED_PLATFORMS}")

    # 3. Format dropdown check
    fmt = asset.get("format", "")
    if fmt not in ALLOWED_FORMATS:
        violations.append(f"Invalid format '{fmt}'. Must be one of: {ALLOWED_FORMATS}")

    # 4. Voice rules & banned claims check
    text_corpus = f"{asset.get('hook', '')} {asset.get('caption', '')}".lower()
    for phrase in BANNED_PHRASES:
        if phrase in text_corpus:
            violations.append(f"Voice violation: Contains banned hyperbolic claim '{phrase}'")

    # 5. Hook quality check (first 2 seconds / first line)
    hook = asset.get("hook", "").strip()
    if len(hook) < 10:
        violations.append("Hook is too short or empty (minimum 10 characters required)")
    if len(hook) > 160:
        violations.append(f"Hook exceeds short-form length limit ({len(hook)} > 160 chars)")

    # 6. Rights check
    rights = asset.get("rights_checked", "")
    if rights != "Yes":
        violations.append(f"Rights issue: rights_checked is '{rights}', must be 'Yes'")

    # 7. AI label needed check
    ai_label = asset.get("ai_label_needed", "")
    if ai_label not in ["Yes", "No"]:
        violations.append(f"Invalid ai_label_needed value '{ai_label}'. Must be 'Yes' or 'No'")

    # 8. Measurability: UTM tracking link & target metric
    utm = asset.get("utm_link", "")
    if not utm.startswith("https://www.incubrix.com/?utm_"):
        violations.append(f"Invalid UTM link format: '{utm}' (must start with https://www.incubrix.com/?utm_)")
    if "utm_campaign=creator_growth_engine_q4" not in utm:
        violations.append("UTM link missing 'utm_campaign=creator_growth_engine_q4'")
    if "utm_content=" not in utm:
        violations.append("UTM link missing 'utm_content=' (asset_id)")

    notes = asset.get("notes", "")
    if not notes.startswith("target_metric="):
        violations.append("Notes must start with 'target_metric=<metric and number>' for measurability")

    # 9. Hashtags and CTA check in caption
    caption = asset.get("caption", "")
    if "#" not in caption:
        violations.append("Caption is missing hashtags")
    cta = asset.get("cta", "")
    if not cta or len(cta.strip()) < 5:
        violations.append("Call to Action (CTA) is missing or too brief")

    # 10. File existence check
    disk_final = asset.get("_disk_final_path")
    if disk_final:
        if not os.path.exists(disk_final):
            violations.append(f"Final asset file does not exist at path: '{disk_final}'")
    elif base_dir:
        final_file = asset.get("final_file_url", "")
        if final_file and not os.path.isabs(final_file):
            final_file = os.path.join(base_dir, final_file)
        if final_file and not os.path.exists(final_file):
            violations.append(f"Final asset file does not exist at path: '{final_file}'")

    disk_source = asset.get("_disk_source_path")
    if disk_source:
        if not os.path.exists(disk_source):
            violations.append(f"Source asset file does not exist at path: '{disk_source}'")
    elif base_dir:
        source_file = asset.get("source_file_url", "")
        if source_file and not os.path.isabs(source_file):
            source_file = os.path.join(base_dir, source_file)
        if source_file and not os.path.exists(source_file):
            violations.append(f"Source asset file does not exist at path: '{source_file}'")

    is_ready = len(violations) == 0
    return is_ready, violations
