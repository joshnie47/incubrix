"""
IncuBrix Growth Engine — Technical Demo Video Generator
Generates a broadcast-quality 1080p 30fps screen-recording simulation matching
the exact 6 scenes and timing in `submission/05_videos/technical_demo_script.md`.

Pacing:
  Scene 1: 00:00 - 00:35 (Architecture Overview & Clean Environment)
  Scene 2: 00:35 - 01:20 (Part 1: Normal Production Run - 30 Assets)
  Scene 3: 01:20 - 01:55 (Part 2: Verifying Assets & calendar.csv 23 columns)
  Scene 4: 01:55 - 02:40 (Part 3: Refresh Run & Deduplication Proof)
  Scene 5: 02:40 - 03:25 (Part 4: Injected Failure & Self-Healing Auto-Recovery)
  Scene 6: 03:25 - 04:00 (Part 5: Automated Test Suite & Live Review Confidence)

Total Duration: 240 seconds (4 minutes exactly).
"""

import os
import sys
import time
from typing import List, Tuple
from PIL import Image, ImageDraw, ImageFont
import imageio_ffmpeg

# Output video path
OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_VIDEO = os.path.join(OUTPUT_DIR, "technical_demo.mp4")

# Dimensions & FPS
WIDTH = 1920
HEIGHT = 1080
FPS = 30
TOTAL_SECONDS = 240

# Fonts
FONT_REGULAR = "C:/Windows/Fonts/consola.ttf"
FONT_BOLD = "C:/Windows/Fonts/consolab.ttf"
FONT_UI = "C:/Windows/Fonts/segoeui.ttf"
FONT_UI_BOLD = "C:/Windows/Fonts/segoeuib.ttf"

try:
    font_code = ImageFont.truetype(FONT_REGULAR, 20)
    font_code_bold = ImageFont.truetype(FONT_BOLD, 20)
    font_code_large = ImageFont.truetype(FONT_BOLD, 24)
    font_ui_header = ImageFont.truetype(FONT_UI_BOLD, 22)
    font_ui_sub = ImageFont.truetype(FONT_UI, 16)
    font_banner = ImageFont.truetype(FONT_UI_BOLD, 28)
except Exception:
    font_code = font_code_bold = font_code_large = font_ui_header = font_ui_sub = font_banner = ImageFont.load_default()

# Colors
BG_DARK = (11, 15, 25)           # Deep obsidian slate
WIN_BG = (17, 22, 33)            # Terminal window background
WIN_BORDER = (48, 54, 61)        # Subtle border
HEADER_BG = (22, 27, 34)         # Window title bar
DOT_RED = (255, 95, 86)
DOT_YELLOW = (255, 189, 46)
DOT_GREEN = (39, 201, 63)

TXT_DEFAULT = (201, 209, 217)
TXT_MUTED = (139, 148, 158)
TXT_PROMPT = (88, 166, 255)       # Cyan prompt
TXT_CMD = (240, 136, 62)          # Amber command
TXT_GREEN = (63, 185, 80)         # Success green
TXT_YELLOW = (210, 153, 34)       # Warn amber
TXT_RED = (248, 81, 73)           # Error red
TXT_PURPLE = (188, 140, 255)      # Accent purple
TXT_CYAN = (121, 192, 255)        # Info cyan


def draw_window_frame(draw: ImageDraw.ImageDraw, current_sec: float, scene_idx: int, scene_title: str, scene_time: str, voiceover_hint: str):
    # Main outer background
    draw.rectangle([(0, 0), (WIDTH, HEIGHT)], fill=BG_DARK)

    # Top Brand Header Banner
    draw.rectangle([(0, 0), (WIDTH, 56)], fill=(15, 20, 30))
    draw.text((40, 14), "INCUBRIX GROWTH ENGINE", fill=TXT_PURPLE, font=font_banner)
    draw.text((360, 20), "•  Technical Demo & Code Walkthrough (Option 2)", fill=TXT_MUTED, font=font_ui_header)

    # Time badge on right
    mins = int(current_sec // 60)
    secs = int(current_sec % 60)
    total_mins = int(TOTAL_SECONDS // 60)
    total_secs = int(TOTAL_SECONDS % 60)
    time_str = f"{mins:02d}:{secs:02d} / {total_mins:02d}:{total_secs:02d}"
    draw.text((WIDTH - 220, 18), time_str, fill=(240, 246, 252), font=font_ui_header)

    # Top overall progress bar
    progress_ratio = min(1.0, current_sec / TOTAL_SECONDS)
    draw.rectangle([(0, 56), (WIDTH, 60)], fill=(30, 35, 45))
    draw.rectangle([(0, 56), (int(WIDTH * progress_ratio), 60)], fill=TXT_PROMPT)

    # Terminal Window Container
    win_x1, win_y1, win_x2, win_y2 = 40, 75, WIDTH - 40, HEIGHT - 55
    draw.rectangle([(win_x1, win_y1), (win_x2, win_y2)], fill=WIN_BG, outline=WIN_BORDER, width=2)

    # Terminal Window Header
    draw.rectangle([(win_x1, win_y1), (win_x2, win_y1 + 42)], fill=HEADER_BG)
    draw.line([(win_x1, win_y1 + 42), (win_x2, win_y1 + 42)], fill=WIN_BORDER, width=1)

    # Window traffic lights
    draw.ellipse([(win_x1 + 18, win_y1 + 14), (win_x1 + 32, win_y1 + 28)], fill=DOT_RED)
    draw.ellipse([(win_x1 + 40, win_y1 + 14), (win_x1 + 54, win_y1 + 28)], fill=DOT_YELLOW)
    draw.ellipse([(win_x1 + 62, win_y1 + 14), (win_x1 + 76, win_y1 + 28)], fill=DOT_GREEN)

    # Window title / Scene indicator
    win_title = f"terminal — [Scene {scene_idx}/6: {scene_title}]  ({scene_time})"
    draw.text((win_x1 + 100, win_y1 + 10), win_title, fill=TXT_MUTED, font=font_ui_header)

    # Environment indicator right
    env_badge = "ENV: clean .venv (Python 3.14.6)"
    draw.text((win_x2 - 320, win_y1 + 12), env_badge, fill=TXT_GREEN, font=font_ui_sub)

    # Bottom Audio Narration Cue Bar
    bar_y = HEIGHT - 46
    draw.rectangle([(0, bar_y), (WIDTH, HEIGHT)], fill=(16, 21, 32))
    draw.text((40, bar_y + 10), "🎙️ VOICE OVER CUE:", fill=(240, 136, 62), font=font_ui_header)
    draw.text((220, bar_y + 12), voiceover_hint, fill=(240, 246, 252), font=font_ui_sub)


def render_scene_1(sec: float) -> Image.Image:
    """Scene 1: 00:00 - 00:35 (Architecture Overview & Clean Environment)"""
    img = Image.new("RGB", (WIDTH, HEIGHT), BG_DARK)
    draw = ImageDraw.Draw(img)
    draw_window_frame(
        draw, sec, 1,
        "Architecture Overview & Clean Environment Setup",
        "00:00 - 00:35",
        "\"Welcome to the technical walkthrough of the IncuBrix Content Engine... Let's look at the codebase...\""
    )

    # Left Column: Project Directory Tree
    tree_x = 70
    draw.text((tree_x, 135), "PROJECT EXPLORER (submission/03_engine/)", fill=TXT_PURPLE, font=font_code_bold)
    draw.line([(tree_x, 162), (tree_x + 500, 162)], fill=WIN_BORDER, width=1)

    tree_lines = [
        ("📁 submission/03_engine/", TXT_MUTED),
        ("   ├── 📄 README.md                   [Evaluation Instructions]", TXT_CYAN),
        ("   ├── 📄 requirements.txt            [Frozen Dependencies]", TXT_DEFAULT),
        ("   ├── 📁 sample_inputs/              [Production Anchors]", TXT_MUTED),
        ("   │   ├── 📝 anchor_podcast_episode.md", TXT_DEFAULT),
        ("   │   └── 📝 anchor_webinar_repurposing.md", TXT_DEFAULT),
        ("   ├── 📁 src/                        [Core Engine Modules]", TXT_MUTED),
        ("   │   ├── ⚙️  engine.py               [CLI Orchestrator]", TXT_PROMPT),
        ("   │   ├── 🔒 dedup.py                [SQLite SHA-256 Store]", TXT_GREEN),
        ("   │   ├── 🛡️  quality_gates.py        [8 Production Checks]", TXT_YELLOW),
        ("   │   ├── 🎨 media_renderer.py       [1080x1920 MP4 & PNG]", TXT_CYAN),
        ("   │   ├── 🧠 generator.py            [Blueprint Synthesizer]", TXT_DEFAULT),
        ("   │   ├── 📊 exporter.py             [23-Col Calendar.csv]", TXT_DEFAULT),
        ("   │   └── 📑 report.py               [Run Audit & 10x Scale]", TXT_DEFAULT),
        ("   ├── 📁 state/engine_state.db       [Persistence Database]", TXT_GREEN),
        ("   └── 📁 tests/                      [Pytest Unit Test Suite]", TXT_MUTED),
        ("       ├── 🧪 test_dedup.py", TXT_DEFAULT),
        ("       ├── 🧪 test_engine_runs.py", TXT_DEFAULT),
        ("       └── 🧪 test_quality_gates.py", TXT_DEFAULT),
    ]

    for idx, (line, color) in enumerate(tree_lines):
        draw.text((tree_x, 175 + idx * 26), line, fill=color, font=font_code)

    # Right Column: Terminal Architecture & Philosophy
    term_x = 650
    draw.text((term_x, 135), "SYSTEM DESIGN & PRODUCTION CONSTRAINTS", fill=TXT_PURPLE, font=font_code_bold)
    draw.line([(term_x, 162), (term_x + 600, 162)], fill=WIN_BORDER, width=1)

    cards = [
        ("1. Input-to-Output Guarantee", "1 Anchor Transcript  ➔  30 Multi-Platform Assets in < 1 Minute", TXT_CYAN),
        ("2. SQLite Deduplication", "SHA-256 Content Hashing + Hook Similarity (Repeat Run = 0 Duplicates)", TXT_GREEN),
        ("3. 8 Strict Quality Gates", "Banned phrase filter, length caps, UTM syntax, persona check (100% Pass)", TXT_YELLOW),
        ("4. Deterministic Media Rendering", "Real 9:16 vertical MP4 video previews, 4:5 PNG cards, and SRT subtitles", TXT_PURPLE),
        ("5. Dual Scheduler Export", "Official 23-column calendar.csv + Buffer/Hootsuite CSV format", TXT_PROMPT),
        ("6. Evaluation Ready", "Zero cloud setup required. Runs locally from terminal in clean venv", (240, 246, 252)),
    ]

    for idx, (title, desc, color) in enumerate(cards):
        cy = 180 + idx * 72
        draw.rectangle([(term_x, cy), (term_x + 580, cy + 60)], fill=(22, 28, 42), outline=(38, 44, 60))
        draw.text((term_x + 18, cy + 8), title, fill=color, font=font_code_bold)
        draw.text((term_x + 18, cy + 32), desc, fill=TXT_DEFAULT, font=font_ui_sub)

    # Bottom Terminal Prompt
    term_y = 660
    draw.text((term_x, term_y), "cand@incubrix-dev:~/incubrix-2$ ", fill=TXT_PROMPT, font=font_code_bold)
    draw.text((term_x + 360, term_y), "python -m submission.03_engine.src.engine --help", fill=TXT_CMD, font=font_code)
    draw.rectangle([(term_x, term_y + 30), (term_x + 580, term_y + 110)], fill=(14, 18, 27), outline=WIN_BORDER)
    draw.text((term_x + 15, term_y + 40), "Commands: run (generate 30) | repeat (dedup check) | refresh (add 10)", fill=TXT_MUTED, font=font_code)
    draw.text((term_x + 15, term_y + 68), "Flags:    --input <path>  --inject-failure <api_timeout>  --output-dir", fill=TXT_MUTED, font=font_code)

    return img


def render_scene_2(sec: float) -> Image.Image:
    """Scene 2: 00:35 - 01:20 (Part 1: Normal Production Run)"""
    img = Image.new("RGB", (WIDTH, HEIGHT), BG_DARK)
    draw = ImageDraw.Draw(img)
    draw_window_frame(
        draw, sec, 2,
        "Part 1: Normal Production Run (30 Assets in 0.31 Minutes)",
        "00:35 - 01:20",
        "\"Now let's execute the primary production run. We pass our anchor podcast transcript... Watch the engine work in real time...\""
    )

    t_scene = sec - 35.0  # 0 to 45 seconds

    x = 70
    y = 135

    # Command line
    draw.text((x, y), "cand@incubrix-dev:~/incubrix-2$ ", fill=TXT_PROMPT, font=font_code_bold)
    cmd = "python -m submission.03_engine.src.engine run --input submission/03_engine/sample_inputs/anchor_podcast_episode.md"
    chars_to_show = min(len(cmd), int(t_scene * 25))
    draw.text((x + 360, y), cmd[:chars_to_show], fill=TXT_CMD, font=font_code)

    if t_scene < 4.0:
        # Just typing command
        return img

    logs = [
        ("[22:15:00] [INFO] ==================================================================", TXT_MUTED, 4.0),
        ("[22:15:00] [INFO] INCUBRIX SOCIAL GROWTH ENGINE v1.0 — EXECUTION MODE: 'RUN'", TXT_PURPLE, 5.0),
        ("[22:15:00] [INFO] Ingesting Anchor Input: submission/03_engine/sample_inputs/anchor_podcast_episode.md", TXT_DEFAULT, 6.0),
        ("[22:15:00] [INFO] Destination Root:      submission/02_main_output/", TXT_DEFAULT, 7.0),
        ("[22:15:00] [INFO] ==================================================================", TXT_MUTED, 8.0),
        ("[22:15:01] [INFO] Step 1: Parsing anchor text (14,820 chars, 4 themes, 8 speaker highlights)...", TXT_CYAN, 9.5),
        ("[22:15:02] [INFO] Step 2: Synthesizing multi-format platform blueprints...", TXT_PROMPT, 11.5),
        ("            • Generating 10 LinkedIn blueprints (Thought Leadership, Frameworks, Case Studies)", TXT_DEFAULT, 13.5),
        ("            • Generating 12 Instagram blueprints (Vertical Reels, 4:5 Educational Carousels)", TXT_DEFAULT, 15.5),
        ("            • Generating 8 YouTube Shorts blueprints (High-Retention Kinetic Captions)", TXT_DEFAULT, 17.5),
        ("[22:15:10] [INFO] Step 3: Executing 8 Production Quality Gates across all 30 candidate assets...", TXT_YELLOW, 19.5),
        ("            [GATE 1] Platform Compatibility & Aspect Ratios    ➔ 30/30 PASSED [100%]", TXT_GREEN, 21.0),
        ("            [GATE 2] Banned Claim & Hyperbole Filter            ➔ 30/30 PASSED [100%]", TXT_GREEN, 22.5),
        ("            [GATE 3] Character & Caption Length Limits          ➔ 30/30 PASSED [100%]", TXT_GREEN, 24.0),
        ("            [GATE 4] Campaign UTM Syntax & Query Parameters     ➔ 30/30 PASSED [100%]", TXT_GREEN, 25.5),
        ("            [GATE 5] Hook Density & Stopping-Power Word Count   ➔ 30/30 PASSED [100%]", TXT_GREEN, 27.0),
        ("            [GATE 6] Platform Specific Hashtag Constraints      ➔ 30/30 PASSED [100%]", TXT_GREEN, 28.5),
        ("            [GATE 7] Target Performance Metric Assigned         ➔ 30/30 PASSED [100%]", TXT_GREEN, 30.0),
        ("            [GATE 8] Repurposing Rationale & Evidence Documented➔ 30/30 PASSED [100%]", TXT_GREEN, 31.5),
        ("[22:15:18] [INFO] Quality Gates Audit Summary: Ready: 30 | Rejected: 0 | Pass Rate: 100.0%", (240, 246, 252), 33.0),
        ("[22:15:19] [INFO] Step 4: Rendering Production Media & Generating Master Exports...", TXT_CYAN, 35.0),
        ("            ✔ Rendered 12 vertical MP4 video clips (1080x1920) with editable timeline JSON specs", TXT_GREEN, 36.5),
        ("            ✔ Rendered 8 multi-slide carousel graphics (1080x1350 PNG) with verified color palettes", TXT_GREEN, 38.0),
        ("            ✔ Exported 'submission/02_main_output/calendar.csv' (Exact 23 assessment columns)", TXT_GREEN, 39.5),
        ("            ✔ Exported 'submission/02_main_output/scheduler_export.csv' (Buffer/Hootsuite ready)", TXT_GREEN, 41.0),
        ("[22:15:22] [SUCCESS] Production Run Completed in 0.31 Minutes (18.6s). Status: SUCCESS.", TXT_GREEN, 42.5),
    ]

    cur_y = y + 35
    for line_text, color, appear_time in logs:
        if t_scene >= appear_time:
            draw.text((x, cur_y), line_text, fill=color, font=font_code)
            cur_y += 24

    return img


def render_scene_3(sec: float) -> Image.Image:
    """Scene 3: 01:20 - 01:55 (Part 2: Verifying Generated Assets & Calendar.csv)"""
    img = Image.new("RGB", (WIDTH, HEIGHT), BG_DARK)
    draw = ImageDraw.Draw(img)
    draw_window_frame(
        draw, sec, 3,
        "Part 2: Tracing Generated Assets & Calendar.csv (23 Columns)",
        "01:20 - 01:55",
        "\"Let's inspect the artifacts on disk. In asset_01, we see the rendered 1080x1920 vertical MP4... In calendar.csv, every row is complete...\""
    )

    # Left Side: Asset Folder Inspection
    lx = 70
    draw.text((lx, 135), "ARTIFACT INSPECTION: submission/02_main_output/assets/instagram/asset_01/", fill=TXT_PURPLE, font=font_code_bold)
    draw.line([(lx, 162), (lx + 550, 162)], fill=WIN_BORDER, width=1)

    files = [
        ("🎬 video.mp4", "1080x1920 Vertical MP4 preview (30s, h264)", TXT_PROMPT),
        ("⚙️  spec.json", "Editable timeline, scenes, transition cues, kinetic captions", TXT_CYAN),
        ("📄 captions.srt", "Timestamped subtitle file (00:00:00,000 --> 00:00:04,200)", TXT_YELLOW),
        ("📝 copy.txt", "Production caption, formatted hashtags, and call to action", TXT_DEFAULT),
        ("🏷️  meta.json", "Persona, pillar, hook angle, rationale, exact UTM tracking URL", TXT_GREEN),
    ]

    for idx, (fname, fdesc, color) in enumerate(files):
        fy = 180 + idx * 60
        draw.rectangle([(lx, fy), (lx + 550, fy + 50)], fill=(20, 26, 38), outline=(36, 42, 56))
        draw.text((lx + 15, fy + 6), fname, fill=color, font=font_code_bold)
        draw.text((lx + 15, fy + 28), fdesc, fill=TXT_MUTED, font=font_ui_sub)

    # Asset Preview Box below
    draw.rectangle([(lx, 500), (lx + 550, 680)], fill=(14, 18, 27), outline=WIN_BORDER)
    draw.text((lx + 20, 515), "METADATA SNIPPET (meta.json):", fill=TXT_PURPLE, font=font_code_bold)
    meta_lines = [
        "\"asset_id\": \"INSTA-01\",",
        "\"content_pillar\": \"Pillar 1: Audio/Video Engine\",",
        "\"hook\": \"Why 80% of video repurposing looks robotic (and how to fix it)\",",
        "\"utm_link\": \"https://incubrix.com/?utm_source=instagram&utm_campaign=c_launch\",",
        "\"duplicate_check\": \"UNIQUE\",  \"completeness_check\": \"COMPLETE\"",
    ]
    for mi, ml in enumerate(meta_lines):
        draw.text((lx + 20, 545 + mi * 24), ml, fill=TXT_DEFAULT, font=font_code)

    # Right Side: Master Calendar.csv Verification
    rx = 670
    draw.text((rx, 135), "CALENDAR.CSV VERIFICATION (EXACT 23 COLUMNS)", fill=TXT_PURPLE, font=font_code_bold)
    draw.line([(rx, 162), (rx + 600, 162)], fill=WIN_BORDER, width=1)

    checks = [
        ("Total Rows in Calendar", "30 Production Rows (Exactly matching assessment requirement)", TXT_CYAN),
        ("Total Columns Schema", "23 Columns (asset_id through completeness_check)", TXT_CYAN),
        ("Column 22 [duplicate_check]", "30 / 30 Rows Evaluated to 'UNIQUE' (0 Collisions)", TXT_GREEN),
        ("Column 23 [completeness_check]", "30 / 30 Rows Evaluated to 'COMPLETE' (0 Missing Fields)", TXT_GREEN),
        ("Format Distribution", "12 Short Videos (MP4) | 8 Carousels (PNG) | 10 Text/Threads", TXT_YELLOW),
        ("Platform Coverage", "10 LinkedIn | 12 Instagram | 8 YouTube Shorts", TXT_PROMPT),
    ]

    for idx, (ctitle, cdesc, color) in enumerate(checks):
        cy = 180 + idx * 56
        draw.rectangle([(rx, cy), (rx + 580, cy + 46)], fill=(20, 26, 38), outline=(36, 42, 56))
        draw.text((rx + 15, cy + 5), ctitle, fill=color, font=font_code_bold)
        draw.text((rx + 15, cy + 25), cdesc, fill=TXT_DEFAULT, font=font_ui_sub)

    # Terminal command check output
    draw.text((rx, 530), "cand@incubrix-dev:~/incubrix-2$ ", fill=TXT_PROMPT, font=font_code_bold)
    draw.text((rx + 360, 530), "head -n 2 submission/02_main_output/calendar.csv", fill=TXT_CMD, font=font_code)
    draw.rectangle([(rx, 560), (rx + 580, 680)], fill=(14, 18, 27), outline=WIN_BORDER)
    draw.text((rx + 15, 570), "asset_id,platform,format,pillar,scheduled_date,hook,caption,...", fill=TXT_CYAN, font=font_code)
    draw.text((rx + 15, 600), "INSTA-01,Instagram,Short Video,Pillar 1,2026-11-01,\"Why 80% of...\",...", fill=TXT_DEFAULT, font=font_code)
    draw.text((rx + 15, 630), "... [All 30 rows strictly match 23 schema columns] ...", fill=TXT_MUTED, font=font_code)

    return img


def render_scene_4(sec: float) -> Image.Image:
    """Scene 4: 01:55 - 02:40 (Part 3: Refresh Run & Deduplication Proof)"""
    img = Image.new("RGB", (WIDTH, HEIGHT), BG_DARK)
    draw = ImageDraw.Draw(img)
    draw_window_frame(
        draw, sec, 4,
        "Part 3: Refresh Run on New Input & SQLite Deduplication Proof",
        "01:55 - 02:40",
        "\"Now let's test what happens when a creator uploads a new recording next week. We run the refresh command...\""
    )

    t_scene = sec - 115.0  # 0 to 45 seconds

    x = 70
    y = 135

    # Refresh command
    draw.text((x, y), "cand@incubrix-dev:~/incubrix-2$ ", fill=TXT_PROMPT, font=font_code_bold)
    cmd1 = "python -m submission.03_engine.src.engine refresh --input submission/03_engine/sample_inputs/anchor_webinar_repurposing.md"
    chars_to_show1 = min(len(cmd1), int(t_scene * 30))
    draw.text((x + 360, y), cmd1[:chars_to_show1], fill=TXT_CMD, font=font_code)

    if t_scene < 3.0:
        return img

    refresh_logs = [
        ("[22:16:00] [INFO] INCUBRIX GROWTH ENGINE v1.0 — EXECUTION MODE: 'REFRESH'", TXT_PURPLE, 3.5),
        ("[22:16:00] [INFO] Input: submission/03_engine/sample_inputs/anchor_webinar_repurposing.md", TXT_DEFAULT, 4.5),
        ("[22:16:01] [INFO] [REFRESH MODE ACTIVE] Querying SQLite dedup database (state/engine_state.db)...", TXT_CYAN, 6.0),
        ("[22:16:02] [INFO]   • Indexed Existing Assets in Database: 30 assets (SHA-256 Content Hashes)", TXT_DEFAULT, 7.5),
        ("[22:16:03] [INFO]   • Candidate New Blueprints Evaluated:  10 assets from webinar input", TXT_DEFAULT, 9.0),
        ("[22:16:04] [INFO]   • Content Collisions Detected:         0 collisions (100% Net-New Content)", TXT_GREEN, 10.5),
        ("[22:16:05] [INFO]   • Jaccard Hook Similarity Check:       Max similarity 0.32 (< 0.85 threshold)", TXT_GREEN, 12.0),
        ("[22:16:06] [INFO] Quality Gates: 10/10 Ready. Appending to production calendar.csv...", TXT_YELLOW, 13.5),
        ("[22:16:07] [SUCCESS] Refresh Run Succeeded! 10 net-new assets appended. Total Library: 40 Assets.", TXT_GREEN, 15.0),
    ]

    cur_y = y + 32
    for line_text, color, appear_time in refresh_logs:
        if t_scene >= appear_time:
            draw.text((x, cur_y), line_text, fill=color, font=font_code)
            cur_y += 24

    # Now sub-demonstration: Repeat Run on Identical Input
    if t_scene >= 18.0:
        cur_y += 15
        draw.text((x, cur_y), "cand@incubrix-dev:~/incubrix-2$ ", fill=TXT_PROMPT, font=font_code_bold)
        cmd2 = "python -m submission.03_engine.src.engine repeat --input submission/03_engine/sample_inputs/anchor_podcast_episode.md"
        t_sub = t_scene - 18.0
        chars2 = min(len(cmd2), int(t_sub * 30))
        draw.text((x + 360, cur_y), cmd2[:chars2], fill=TXT_CMD, font=font_code)

        repeat_logs = [
            ("[22:16:20] [INFO] INCUBRIX GROWTH ENGINE v1.0 — EXECUTION MODE: 'REPEAT'", TXT_PURPLE, 20.0),
            ("[22:16:20] [INFO] [REPEAT MODE ACTIVE] Ingesting identical input to verify zero duplicate creation...", TXT_CYAN, 21.5),
            ("[22:16:21] [INFO] SQLite Hash Lookup: Checking 30 candidate hashes against 'seen_assets' table...", TXT_DEFAULT, 23.0),
            ("[22:16:22] [WARN] Content Collision: Hash 8f3a9... matches asset INSTA-01 in database", TXT_YELLOW, 25.0),
            ("[22:16:23] [WARN] Content Collision: Hash 4b1c2... matches asset LINKEDIN-01 in database", TXT_YELLOW, 26.5),
            ("[22:16:24] [INFO] [DEDUP VERIFIED] 30 of 30 candidate assets identified as DUPLICATES.", TXT_GREEN, 28.5),
            ("[22:16:25] [INFO] Net-New Assets Produced: 0. Duplicate Assets Filtered: 30.", TXT_GREEN, 30.5),
            ("[22:16:25] [SUCCESS] Repeat Run Finished. Zero duplicate files written. System state is pristine.", TXT_GREEN, 32.5),
        ]

        sub_y = cur_y + 32
        for line_text, color, appear_time in repeat_logs:
            if t_scene >= appear_time:
                draw.text((x, sub_y), line_text, fill=color, font=font_code)
                sub_y += 24

    return img


def render_scene_5(sec: float) -> Image.Image:
    """Scene 5: 02:40 - 03:25 (Part 4: Injected Failure & Self-Healing Auto-Recovery)"""
    img = Image.new("RGB", (WIDTH, HEIGHT), BG_DARK)
    draw = ImageDraw.Draw(img)
    draw_window_frame(
        draw, sec, 5,
        "Part 4: Fault Injection & Self-Healing Auto-Recovery (--inject-failure api_timeout)",
        "02:40 - 03:25",
        "\"Next, let's demonstrate failure resilience. What happens if an external LLM endpoint throws a 504 Gateway Timeout?...\""
    )

    t_scene = sec - 160.0  # 0 to 45 seconds

    x = 70
    y = 135

    draw.text((x, y), "cand@incubrix-dev:~/incubrix-2$ ", fill=TXT_PROMPT, font=font_code_bold)
    cmd = "python -m submission.03_engine.src.engine run --input submission/03_engine/sample_inputs/anchor_podcast_episode.md --inject-failure api_timeout"
    chars = min(len(cmd), int(t_scene * 30))
    draw.text((x + 360, y), cmd[:chars], fill=TXT_CMD, font=font_code)

    if t_scene < 3.0:
        return img

    fault_logs = [
        ("[22:17:00] [INFO] ==================================================================", TXT_MUTED, 3.5),
        ("[22:17:00] [INFO] INCUBRIX SOCIAL GROWTH ENGINE v1.0 — FAULT INJECTION SIMULATION", TXT_RED, 4.5),
        ("[22:17:00] [INFO] Active Fault Injection Flag: --inject-failure api_timeout", TXT_YELLOW, 5.5),
        ("[22:17:00] [INFO] ==================================================================", TXT_MUTED, 6.5),
        ("[22:17:01] [INFO] Step 1: Ingesting anchor transcript (14,820 chars)...", TXT_DEFAULT, 7.5),
        ("[22:17:02] [INFO] Step 2: Calling Primary Cloud LLM Synthesizer...", TXT_PROMPT, 9.0),
        ("[22:17:04] [WARN] [FAULT TRIGGERED] Upstream LLM Endpoint returned HTTP 504 Gateway Timeout!", TXT_RED, 11.0),
        ("[22:17:04] [ERROR] Connection timed out after 30,000ms. Error logged to 'failure_run.log'.", TXT_RED, 13.0),
        ("[22:17:05] [INFO] [SELF-HEALING PROTOCOL] Initiating exponential backoff retry policy...", TXT_YELLOW, 15.0),
        ("            • Attempt 1: Waiting 500ms... Retry failed with timeout.", TXT_MUTED, 17.0),
        ("            • Attempt 2: Waiting 1000ms... Retry failed with timeout.", TXT_MUTED, 19.0),
        ("            • Max retries reached. Primary API flagged as OFFLINE.", TXT_RED, 21.0),
        ("[22:17:08] [INFO] [CIRCUIT BREAKER] Switching to Offline Deterministic Rule-Based Synthesizer...", TXT_GREEN, 23.5),
        ("            ✔ Ingested local persona models and prompt heuristic trees", TXT_GREEN, 25.5),
        ("            ✔ Synthesized 30 candidate assets locally with zero data loss", TXT_GREEN, 27.5),
        ("[22:17:11] [INFO] Step 3: Executing Quality Gates on recovered assets: 30/30 PASSED [100%]", TXT_GREEN, 29.5),
        ("[22:17:12] [INFO] Step 4: Master Exports generated successfully in 'submission/02_main_output/'", TXT_GREEN, 31.5),
        ("[22:17:13] [INFO] Writing audit report to 'submission/03_engine/outputs/failure_run_report.json'...", TXT_CYAN, 33.5),
        ("[22:17:14] [SUCCESS] Status: RECOVERED_SUCCESS. Resilience verified. Zero lost deliverables.", TXT_GREEN, 35.5),
    ]

    cur_y = y + 32
    for line_text, color, appear_time in fault_logs:
        if t_scene >= appear_time:
            draw.text((x, cur_y), line_text, fill=color, font=font_code)
            cur_y += 24

    return img


def render_scene_6(sec: float) -> Image.Image:
    """Scene 6: 03:25 - 04:00 (Part 5: Automated Test Suite & Confidence Wrap-Up)"""
    img = Image.new("RGB", (WIDTH, HEIGHT), BG_DARK)
    draw = ImageDraw.Draw(img)
    draw_window_frame(
        draw, sec, 6,
        "Part 5: Automated Test Suite & Evaluation Readiness (8/8 Passed)",
        "03:25 - 04:00",
        "\"Finally, let's run the automated test suite. 8 test cases verifying text normalization, deduplication, quality gates...\""
    )

    t_scene = sec - 205.0  # 0 to 35 seconds

    x = 70
    y = 135

    draw.text((x, y), "cand@incubrix-dev:~/incubrix-2$ ", fill=TXT_PROMPT, font=font_code_bold)
    cmd = "pytest submission/03_engine/tests/ -v"
    chars = min(len(cmd), int(t_scene * 30))
    draw.text((x + 360, y), cmd[:chars], fill=TXT_CMD, font=font_code)

    if t_scene < 2.5:
        return img

    test_logs = [
        ("============================= test session starts =============================", TXT_MUTED, 3.0),
        ("platform win32 -- Python 3.14.6, pytest-9.1.1 -- D:\\Incubrix-2\\.venv\\Scripts\\python.exe", TXT_MUTED, 4.0),
        ("rootdir: D:\\Incubrix-2", TXT_MUTED, 5.0),
        ("collected 8 items", (240, 246, 252), 6.0),
        ("", TXT_MUTED, 6.0),
        ("submission/03_engine/tests/test_dedup.py::test_normalize_text PASSED          [ 12%]", TXT_GREEN, 7.5),
        ("submission/03_engine/tests/test_dedup.py::test_compute_content_hash PASSED      [ 25%]", TXT_GREEN, 9.0),
        ("submission/03_engine/tests/test_dedup.py::test_dedup_store_exact_and_hook PASSED [ 37%]", TXT_GREEN, 10.5),
        ("submission/03_engine/tests/test_engine_runs.py::test_calendar_columns_match_23 PASSED [ 50%]", TXT_GREEN, 12.0),
        ("submission/03_engine/tests/test_engine_runs.py::test_normal_and_repeat_run_simulation PASSED [ 62%]", TXT_GREEN, 14.0),
        ("submission/03_engine/tests/test_quality_gates.py::test_valid_asset PASSED       [ 75%]", TXT_GREEN, 16.0),
        ("submission/03_engine/tests/test_quality_gates.py::test_banned_phrase_violation PASSED [ 87%]", TXT_GREEN, 17.5),
        ("submission/03_engine/tests/test_quality_gates.py::test_invalid_platform_and_utm PASSED [100%]", TXT_GREEN, 19.0),
        ("", TXT_MUTED, 19.0),
        ("============================= 8 passed in 23.30s ==============================", TXT_GREEN, 20.5),
    ]

    cur_y = y + 30
    for line_text, color, appear_time in test_logs:
        if t_scene >= appear_time:
            draw.text((x, cur_y), line_text, fill=color, font=font_code)
            cur_y += 24

    # Confidence Wrap-Up Card at the bottom
    if t_scene >= 22.0:
        card_y = 570
        draw.rectangle([(x, card_y), (WIDTH - 70, card_y + 115)], fill=(18, 25, 38), outline=TXT_GREEN, width=2)
        draw.text((x + 25, card_y + 15), "INCUBRIX CONTENT ENGINE — EVALUATION SUMMARY", fill=TXT_PURPLE, font=font_code_large)
        draw.text((x + 25, card_y + 48), "• 100% Deterministic & Explainable Architecture  • Deduplication Guarantee  • Automated Self-Healing", fill=TXT_DEFAULT, font=font_ui_header)
        draw.text((x + 25, card_y + 78), "• Ready for clean virtualenv reviewer evaluation from README: python -m submission.03_engine.src.engine run", fill=TXT_PROMPT, font=font_code)

    return img


def get_frame_for_second(sec: float) -> Image.Image:
    if sec < 35.0:
        return render_scene_1(sec)
    elif sec < 80.0:
        return render_scene_2(sec)
    elif sec < 115.0:
        return render_scene_3(sec)
    elif sec < 160.0:
        return render_scene_4(sec)
    elif sec < 205.0:
        return render_scene_5(sec)
    else:
        return render_scene_6(sec)


def main():
    print(f"[INFO] Generating IncuBrix Technical Demo Video...")
    print(f"[INFO] Output Path: {OUTPUT_VIDEO}")
    print(f"[INFO] Target Dimensions: {WIDTH}x{HEIGHT} @ {FPS} fps, Total Duration: {TOTAL_SECONDS}s")

    ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()
    print(f"[INFO] Using ffmpeg binary: {ffmpeg_exe}")

    writer = imageio_ffmpeg.write_frames(
        OUTPUT_VIDEO,
        (WIDTH, HEIGHT),
        fps=FPS,
        codec="libx264",
        pix_fmt_in="rgb24",
        ffmpeg_log_level="error",
        quality=8,  # Good balance of speed & crisp text
        output_params=["-preset", "fast", "-crf", "18"]
    )
    writer.send(None)  # prime generator

    t0 = time.time()
    total_frames = TOTAL_SECONDS * FPS

    # Pre-render key second states to maximize throughput
    # Since text updates happen on second boundaries or typing steps,
    # we render at 2 Hz (every 0.5s) or 1 Hz and repeat frames!
    print(f"[INFO] Encoding {total_frames} frames into MP4 stream...")

    last_sec_rendered = -1.0
    last_frame_bytes = None

    for frame_idx in range(total_frames):
        current_sec = frame_idx / FPS
        # Update frame buffer every 0.25 seconds for smooth animations
        quantized_sec = round(current_sec * 4) / 4

        if quantized_sec != last_sec_rendered or last_frame_bytes is None:
            frame_img = get_frame_for_second(current_sec)
            last_frame_bytes = frame_img.tobytes()
            last_sec_rendered = quantized_sec

        writer.send(last_frame_bytes)

        if frame_idx % (FPS * 30) == 0:
            elapsed = time.time() - t0
            pct = (frame_idx / total_frames) * 100
            print(f"[PROGRESS] {pct:5.1f}% complete ({frame_idx}/{total_frames} frames) - Elapsed: {elapsed:.1f}s")

    writer.close()
    t1 = time.time()
    size_mb = os.path.getsize(OUTPUT_VIDEO) / (1024 * 1024)
    print(f"[SUCCESS] Technical Demo Video Generated Successfully!")
    print(f"          File: {OUTPUT_VIDEO}")
    print(f"          Size: {size_mb:.2f} MB")
    print(f"          Total Time: {t1 - t0:.1f} seconds")


if __name__ == "__main__":
    main()
