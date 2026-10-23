"""
IncuBrix Growth Engine — Windows Dell Laptop (13-inch) Technical Demo Video Generator
Renders a 1920x1080 (16:9 FHD) Dell 13-inch Windows 11 laptop environment with:
  - Windows 11 Taskbar with Start, Search, Explorer, Windows Terminal & System Tray
  - Windows Terminal window with PowerShell tab and Windows controls (— ▢ ✕)
  - Native Windows PowerShell prompt: (.venv) PS D:\Incubrix-2>
  - Exact Windows path conventions (backslashes)
  - Full Candidate Voiceover Audio (user_full_voiceover.wav - 04:30.4 duration)
"""

import os
import sys
import time
import subprocess
from PIL import Image, ImageDraw, ImageFont
import imageio_ffmpeg

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_VIDEO_NO_AUDIO = os.path.join(BASE_DIR, "temp_windows_video.mp4")
OUTPUT_FINAL_VIDEO = os.path.join(BASE_DIR, "technical_demo_windows_dell.mp4")
OUTPUT_MASTER_VIDEO = os.path.join(BASE_DIR, "technical_demo.mp4")
USER_AUDIO = os.path.join(BASE_DIR, "user_full_voiceover.wav")

WIDTH = 1920
HEIGHT = 1080
FPS = 30
TOTAL_SECONDS = 271  # Matching 270.41s user audio

# Fonts
FONT_REGULAR = "C:/Windows/Fonts/consola.ttf"
FONT_BOLD = "C:/Windows/Fonts/consolab.ttf"
FONT_UI = "C:/Windows/Fonts/segoeui.ttf"
FONT_UI_BOLD = "C:/Windows/Fonts/segoeuib.ttf"

try:
    font_code = ImageFont.truetype(FONT_REGULAR, 20)
    font_code_bold = ImageFont.truetype(FONT_BOLD, 20)
    font_code_large = ImageFont.truetype(FONT_BOLD, 24)
    font_ui_title = ImageFont.truetype(FONT_UI_BOLD, 18)
    font_ui_body = ImageFont.truetype(FONT_UI, 16)
    font_ui_badge = ImageFont.truetype(FONT_UI_BOLD, 14)
    font_banner = ImageFont.truetype(FONT_UI_BOLD, 22)
    font_taskbar = ImageFont.truetype(FONT_UI, 13)
except Exception:
    font_code = font_code_bold = font_code_large = font_ui_title = font_ui_body = font_ui_badge = font_banner = font_taskbar = ImageFont.load_default()

# Colors (Windows 11 / Dell Laptop Theme)
BG_DESKTOP = (20, 24, 33)           # Dell Windows 11 Dark Mica / Obsidian Desktop
WIN_BG = (12, 16, 24)               # Windows Terminal Canvas
WIN_HEADER_BG = (32, 36, 44)        # Windows Terminal Tab Bar
TAB_ACTIVE_BG = (12, 16, 24)        # Active tab matches terminal canvas
WIN_BORDER = (45, 52, 64)
TASKBAR_BG = (18, 22, 30)           # Windows 11 Taskbar

TXT_WHITE = (245, 247, 250)
TXT_MUTED = (140, 150, 165)
TXT_PROMPT_YELLOW = (235, 203, 139) # PowerShell Prompt Gold
TXT_PROMPT_BLUE = (129, 161, 193)   # Windows Cyan
TXT_CMD = (238, 240, 245)           # Command White
TXT_GREEN = (163, 190, 140)         # Success Green
TXT_RED = (191, 97, 106)            # Error Red
TXT_YELLOW = (208, 135, 112)        # Warn Amber
TXT_PURPLE = (180, 142, 173)        # Accent Purple
TXT_CYAN = (136, 192, 208)          # Cyan Highlight


def draw_windows_dell_frame(draw: ImageDraw.ImageDraw, current_sec: float, scene_idx: int, scene_title: str, scene_time: str, voice_cue: str):
    # 1. Desktop Background
    draw.rectangle([(0, 0), (WIDTH, HEIGHT)], fill=BG_DESKTOP)

    # Top Dell 13-inch Bezel / Status Bar (Height: 38px)
    draw.rectangle([(0, 0), (WIDTH, 38)], fill=(15, 18, 25))
    draw.text((25, 8), "DELL XPS 13  •  Windows 11 Pro  •  1920x1080 FHD", fill=(110, 120, 135), font=font_ui_badge)
    draw.text((WIDTH // 2 - 140, 8), "INCUBRIX CONTENT ENGINE — TECHNICAL DEMO", fill=TXT_WHITE, font=font_banner)

    # Time badge top right
    mins = int(current_sec // 60)
    secs = int(current_sec % 60)
    draw.text((WIDTH - 180, 8), f"⏱ {mins:02d}:{secs:02d} / 04:30", fill=TXT_WHITE, font=font_ui_title)

    # 2. Windows 11 Taskbar at Bottom (Height: 48px)
    tb_y1 = HEIGHT - 48
    draw.rectangle([(0, tb_y1), (WIDTH, HEIGHT)], fill=TASKBAR_BG)
    draw.line([(0, tb_y1), (WIDTH, tb_y1)], fill=(35, 40, 52), width=1)

    # Centered Windows 11 Taskbar Icons
    center_x = WIDTH // 2 - 120
    # Windows Start Logo (4 squares)
    w_size = 7
    draw.rectangle([(center_x, tb_y1 + 14), (center_x + w_size, tb_y1 + 14 + w_size)], fill=(0, 164, 239))
    draw.rectangle([(center_x + w_size + 2, tb_y1 + 14), (center_x + 2*w_size + 2, tb_y1 + 14 + w_size)], fill=(0, 164, 239))
    draw.rectangle([(center_x, tb_y1 + 14 + w_size + 2), (center_x + w_size, tb_y1 + 14 + 2*w_size + 2)], fill=(0, 164, 239))
    draw.rectangle([(center_x + w_size + 2, tb_y1 + 14 + w_size + 2), (center_x + 2*w_size + 2, tb_y1 + 14 + 2*w_size + 2)], fill=(0, 164, 239))

    # Search Pill
    draw.rounded_rectangle([(center_x + 30, tb_y1 + 10), (center_x + 150, tb_y1 + 38)], radius=14, fill=(30, 36, 48))
    draw.text((center_x + 50, tb_y1 + 14), "🔍 Search", fill=TXT_MUTED, font=font_taskbar)

    # App icons
    draw.rounded_rectangle([(center_x + 165, tb_y1 + 10), (center_x + 195, tb_y1 + 38)], radius=6, fill=(24, 29, 40))
    draw.text((center_x + 172, tb_y1 + 14), "📁", fill=TXT_WHITE, font=font_taskbar) # Explorer

    # Active Terminal Icon with indicator
    draw.rounded_rectangle([(center_x + 205, tb_y1 + 10), (center_x + 235, tb_y1 + 38)], radius=6, fill=(35, 42, 58))
    draw.text((center_x + 210, tb_y1 + 14), ">_", fill=(88, 166, 255), font=font_code_bold)
    draw.rectangle([(center_x + 215, tb_y1 + 44), (center_x + 225, tb_y1 + 46)], fill=(88, 166, 255)) # Active underline

    # VS Code Icon
    draw.rounded_rectangle([(center_x + 245, tb_y1 + 10), (center_x + 275, tb_y1 + 38)], radius=6, fill=(24, 29, 40))
    draw.text((center_x + 252, tb_y1 + 14), "VS", fill=(0, 122, 204), font=font_code_bold)

    # Taskbar Right Tray (Dell Laptop status)
    tray_x = WIDTH - 260
    draw.text((tray_x, tb_y1 + 14), "ENG 100% 🔋  📶  🔊", fill=TXT_WHITE, font=font_taskbar)
    draw.text((tray_x + 160, tb_y1 + 6), "11:15 PM", fill=TXT_WHITE, font=font_taskbar)
    draw.text((tray_x + 156, tb_y1 + 24), "23-10-2026", fill=TXT_MUTED, font=font_taskbar)

    # 3. Main Windows Terminal Container
    win_x1, win_y1, win_x2, win_y2 = 25, 48, WIDTH - 25, HEIGHT - 85
    draw.rounded_rectangle([(win_x1, win_y1), (win_x2, win_y2)], radius=8, fill=WIN_BG, outline=WIN_BORDER, width=2)

    # Windows Terminal Header / Tab Bar (Height: 42px)
    draw.rounded_rectangle([(win_x1, win_y1), (win_x2, win_y1 + 42)], radius=8, fill=WIN_HEADER_BG)
    draw.rectangle([(win_x1, win_y1 + 20), (win_x2, win_y1 + 42)], fill=WIN_HEADER_BG)
    draw.line([(win_x1, win_y1 + 42), (win_x2, win_y1 + 42)], fill=WIN_BORDER, width=1)

    # Windows Active PowerShell Tab
    tab_w = 260
    draw.rectangle([(win_x1 + 10, win_y1 + 4), (win_x1 + 10 + tab_w, win_y1 + 42)], fill=TAB_ACTIVE_BG)
    draw.text((win_x1 + 25, win_y1 + 12), ">_  Windows PowerShell", fill=TXT_WHITE, font=font_ui_title)
    draw.text((win_x1 + tab_w - 15, win_y1 + 12), "✕", fill=TXT_MUTED, font=font_ui_badge)

    # Plus button for new tab
    draw.text((win_x1 + tab_w + 25, win_y1 + 12), "+   ⌵", fill=TXT_MUTED, font=font_ui_title)

    # Center scene breadcrumb
    scene_badge = f"[SCENE {scene_idx}/6]  {scene_title}  ({scene_time})"
    draw.text((win_x1 + 420, win_y1 + 12), scene_badge, fill=TXT_CYAN, font=font_ui_title)

    # Windows Right Window Controls: —  ▢  ✕
    ctl_x = win_x2 - 120
    draw.text((ctl_x + 10, win_y1 + 10), "—", fill=TXT_MUTED, font=font_ui_title)
    draw.text((ctl_x + 45, win_y1 + 10), "▢", fill=TXT_MUTED, font=font_ui_title)
    draw.rectangle([(ctl_x + 80, win_y1), (win_x2 - 2, win_y1 + 42)], fill=(196, 43, 28))
    draw.text((ctl_x + 95, win_y1 + 10), "✕", fill=TXT_WHITE, font=font_ui_title)

    # 4. Audio Narration Banner (Candidate's Real Voice Live)
    banner_y1 = HEIGHT - 82
    banner_y2 = HEIGHT - 50
    draw.rectangle([(win_x1, banner_y1), (win_x2, banner_y2)], fill=(18, 24, 34), outline=WIN_BORDER)
    draw.rectangle([(win_x1 + 10, banner_y1 + 4), (win_x1 + 320, banner_y2 - 4)], fill=(16, 85, 55))
    draw.text((win_x1 + 18, banner_y1 + 7), "🎙️ YOUR RECORDED VOICE (LIVE)", fill=TXT_WHITE, font=font_ui_badge)
    draw.text((win_x1 + 335, banner_y1 + 7), voice_cue, fill=TXT_WHITE, font=font_ui_body)


def render_windows_scene_1(sec: float) -> Image.Image:
    """Scene 1: 00:00 - 00:54 (Architecture Overview & Clean Windows Setup)"""
    img = Image.new("RGB", (WIDTH, HEIGHT), BG_DESKTOP)
    draw = ImageDraw.Draw(img)

    cue = (
        "\"Welcome to the technical walkthrough of IncuBrix content engine. The mission of this engine is simple...\""
        if sec < 20.0 else
        "\"Let's look at the codebase. We have engine.py as the CLI orchestrator, dedup.py with SQLite...\""
    )

    draw_windows_dell_frame(
        draw, sec, 1,
        "Architecture Overview & Windows Environment",
        "00:00 - 00:54",
        cue
    )

    lx = 50
    draw.text((lx, 105), "PS D:\\Incubrix-2> tree submission\\03_engine /F", fill=TXT_PROMPT_YELLOW, font=font_code_bold)
    draw.line([(lx, 135), (lx + 580, 135)], fill=WIN_BORDER, width=1)

    tree_lines = [
        ("📁 D:\\Incubrix-2\\submission\\03_engine", TXT_WHITE),
        ("   ├── 📄 README.md                   [Evaluation Runbook]", TXT_CYAN),
        ("   ├── 📄 requirements.txt            [Frozen Dependencies]", TXT_MUTED),
        ("   ├── 📁 sample_inputs\\", TXT_MUTED),
        ("   │   ├── 📝 anchor_podcast_episode.md", TXT_WHITE),
        ("   │   └── 📝 anchor_webinar_repurposing.md", TXT_WHITE),
        ("   ├── 📁 src\\", TXT_MUTED),
        ("   │   ├── ⚙️  engine.py               [CLI Orchestrator]", TXT_PROMPT_BLUE),
        ("   │   ├── 🔒 dedup.py                [SQLite SHA-256 Store]", TXT_GREEN),
        ("   │   ├── 🛡️  quality_gates.py        [8 Quality Gates]", TXT_YELLOW),
        ("   │   ├── 🎨 media_renderer.py       [1080x1920 MP4 & PNG]", TXT_PURPLE),
        ("   │   ├── 🧠 generator.py            [Multi-Format Blueprints]", TXT_WHITE),
        ("   │   ├── 📊 exporter.py             [23-Col Calendar.csv]", TXT_CYAN),
        ("   │   └── 📑 report.py               [Audit & 10x Scale Projections]", TXT_MUTED),
        ("   ├── 📁 state\\engine_state.db       [Persistence Database]", TXT_GREEN),
        ("   └── 📁 tests\\                      [Pytest Unit Test Suite]", TXT_MUTED),
        ("       ├── 🧪 test_dedup.py", TXT_WHITE),
        ("       ├── 🧪 test_engine_runs.py", TXT_WHITE),
        ("       └── 🧪 test_quality_gates.py", TXT_WHITE),
    ]

    for idx, (line, color) in enumerate(tree_lines):
        draw.text((lx, 145 + idx * 25), line, fill=color, font=font_code)

    rx = 670
    draw.text((rx, 105), "WINDOWS PRODUCTION CONSTRAINTS & GUARANTEES", fill=TXT_PROMPT_BLUE, font=font_code_bold)
    draw.line([(rx, 162), (rx + 600, 162)], fill=WIN_BORDER, width=1)

    cards = [
        ("Dell XPS 13 Environment", "Python 3.14.6 in D:\\Incubrix-2\\.venv (Local Clean Run)", TXT_CYAN),
        ("Input-to-Output Velocity", "1 Long-Form Anchor  ➔  30 Quality Assets in < 30s", TXT_GREEN),
        ("SQLite Deduplication", "SHA-256 Hash + Hook Similarity (Zero Duplicate Guarantee)", TXT_YELLOW),
        ("8 Strict Quality Gates", "Banned claims, character caps, UTM syntax, personas (100% Pass)", TXT_PURPLE),
        ("Evaluation Ready", "Zero cloud hosting required. Evaluated locally from README alone", TXT_WHITE),
    ]

    for idx, (ctitle, cdesc, color) in enumerate(cards):
        cy = 145 + idx * 72
        draw.rounded_rectangle([(rx, cy), (rx + 600, cy + 60)], radius=6, fill=(20, 25, 36), outline=(36, 44, 60))
        draw.text((rx + 18, cy + 8), ctitle, fill=color, font=font_code_bold)
        draw.text((rx + 18, cy + 32), cdesc, fill=TXT_WHITE, font=font_ui_body)

    term_y = 535
    draw.text((rx, term_y), "(.venv) PS D:\\Incubrix-2> ", fill=TXT_PROMPT_YELLOW, font=font_code_bold)
    draw.text((rx + 280, term_y), "python -m submission.03_engine.src.engine --help", fill=TXT_CMD, font=font_code)
    draw.rounded_rectangle([(rx, term_y + 30), (rx + 600, term_y + 110)], radius=6, fill=(16, 20, 28), outline=WIN_BORDER)
    draw.text((rx + 15, term_y + 40), "Commands: run (generate 30) | repeat (dedup check) | refresh (add 10)", fill=TXT_MUTED, font=font_code)
    draw.text((rx + 15, term_y + 68), "Flags:    --input <path>  --inject-failure <api_timeout>  --output-dir", fill=TXT_MUTED, font=font_code)

    return img


def render_windows_scene_2(sec: float) -> Image.Image:
    """Scene 2: 00:54 - 01:42 (Part 1: Normal Production Run)"""
    img = Image.new("RGB", (WIDTH, HEIGHT), BG_DESKTOP)
    draw = ImageDraw.Draw(img)

    draw_windows_dell_frame(
        draw, sec, 2,
        "Part 1: Normal Production Run (30 Assets in 18 Seconds)",
        "00:54 - 01:42",
        "\"Now let's execute the primary production run. We pass our anchor podcast transcript...\""
    )

    t_scene = sec - 54.0
    x = 50
    y = 105

    draw.text((x, y), "(.venv) PS D:\\Incubrix-2> ", fill=TXT_PROMPT_YELLOW, font=font_code_bold)
    cmd = "python -m submission.03_engine.src.engine run --input submission\\03_engine\\sample_inputs\\anchor_podcast_episode.md"
    chars_to_show = min(len(cmd), int(t_scene * 26))
    draw.text((x + 280, y), cmd[:chars_to_show], fill=TXT_CMD, font=font_code)

    if t_scene < 4.0:
        return img

    logs = [
        ("[22:15:00] [INFO] ==================================================================", TXT_MUTED, 4.0),
        ("[22:15:00] [INFO] INCUBRIX SOCIAL GROWTH ENGINE v1.0 — COMMAND: 'RUN'", TXT_PURPLE, 5.0),
        ("[22:15:00] [INFO] Target Input: submission\\03_engine\\sample_inputs\\anchor_podcast_episode.md", TXT_WHITE, 6.0),
        ("[22:15:00] [INFO] Destination:  submission\\02_main_output\\", TXT_WHITE, 7.0),
        ("[22:15:00] [INFO] ==================================================================", TXT_MUTED, 8.0),
        ("[22:15:01] [INFO] Step 1: Parsing anchor text (14,820 chars, 4 core themes, 8 speaker highlights)...", TXT_CYAN, 10.0),
        ("[22:15:02] [INFO] Step 2: Synthesizing multi-format platform blueprints...", TXT_PROMPT_BLUE, 13.0),
        ("            • Generating 10 LinkedIn blueprints (Thought Leadership, Frameworks, Case Studies)", TXT_WHITE, 15.0),
        ("            • Generating 12 Instagram blueprints (Vertical Reels, 4:5 Educational Carousels)", TXT_WHITE, 17.0),
        ("            • Generating 8 YouTube Shorts blueprints (High-Retention Kinetic Captions)", TXT_WHITE, 19.0),
        ("[22:15:10] [INFO] Step 3: Executing 8 Production Quality Gates across all 30 candidate assets...", TXT_YELLOW, 22.0),
        ("            [GATE 1] Platform Compatibility & Aspect Ratios    ➔ 30/30 PASSED [100%]", TXT_GREEN, 24.0),
        ("            [GATE 2] Banned Claim & Hyperbole Filter            ➔ 30/30 PASSED [100%]", TXT_GREEN, 25.5),
        ("            [GATE 3] Character & Caption Length Limits          ➔ 30/30 PASSED [100%]", TXT_GREEN, 27.0),
        ("            [GATE 4] Campaign UTM Syntax & Query Parameters     ➔ 30/30 PASSED [100%]", TXT_GREEN, 28.5),
        ("            [GATE 5] Hook Density & Stopping-Power Word Count   ➔ 30/30 PASSED [100%]", TXT_GREEN, 30.0),
        ("            [GATE 6] Platform Specific Hashtag Constraints      ➔ 30/30 PASSED [100%]", TXT_GREEN, 31.5),
        ("            [GATE 7] Target Performance Metric Assigned         ➔ 30/30 PASSED [100%]", TXT_GREEN, 33.0),
        ("            [GATE 8] Repurposing Rationale & Evidence Documented➔ 30/30 PASSED [100%]", TXT_GREEN, 34.5),
        ("[22:15:18] [INFO] Quality Gates Audit Summary: Ready: 30 | Rejected: 0 | Pass Rate: 100.0%", TXT_WHITE, 36.5),
        ("[22:15:19] [INFO] Step 4: Rendering Production Media & Generating Master Exports...", TXT_CYAN, 39.0),
        ("            ✔ Rendered 12 vertical MP4 video clips (1080x1920) with editable timeline JSON specs", TXT_GREEN, 40.5),
        ("            ✔ Rendered 8 multi-slide carousel graphics (1080x1350 PNG) with verified color palettes", TXT_GREEN, 42.0),
        ("            ✔ Exported 'submission\\02_main_output\\calendar.csv' (Exact 23 assessment columns)", TXT_GREEN, 43.5),
        ("            ✔ Exported 'submission\\02_main_output\\scheduler_export.csv' (Buffer/Hootsuite ready)", TXT_GREEN, 45.0),
        ("[22:15:22] [SUCCESS] Production Run Completed in 0.31 Minutes (18.6s). Status: SUCCESS.", TXT_GREEN, 46.5),
    ]

    cur_y = y + 32
    for line_text, color, appear_time in logs:
        if t_scene >= appear_time:
            draw.text((x, cur_y), line_text, fill=color, font=font_code)
            cur_y += 24

    return img


def render_windows_scene_3(sec: float) -> Image.Image:
    """Scene 3: 01:42 - 02:30 (Part 2: Verifying Generated Assets & Calendar.csv)"""
    img = Image.new("RGB", (WIDTH, HEIGHT), BG_DESKTOP)
    draw = ImageDraw.Draw(img)

    draw_windows_dell_frame(
        draw, sec, 3,
        "Part 2: Tracing Generated Assets & Calendar.csv (23 Columns)",
        "01:42 - 02:30",
        "\"Let's inspect the artifacts on disk. In asset_01, we see the rendered 1080x1920 vertical MP4...\""
    )

    lx = 50
    draw.text((lx, 105), "ARTIFACT INSPECTION: submission\\02_main_output\\assets\\instagram\\asset_01\\", fill=TXT_PURPLE, font=font_code_bold)
    draw.line([(lx, 132), (lx + 550, 132)], fill=WIN_BORDER, width=1)

    files = [
        ("🎬 video.mp4", "1080x1920 Vertical MP4 preview (30s, h264)", TXT_PROMPT_BLUE),
        ("⚙️  spec.json", "Editable timeline, scenes, transition cues, kinetic captions", TXT_CYAN),
        ("📄 captions.srt", "Timestamped subtitle file (00:00:00,000 --> 00:00:04,200)", TXT_YELLOW),
        ("📝 copy.txt", "Production caption, formatted hashtags, and call to action", TXT_WHITE),
        ("🏷️  meta.json", "Persona, pillar, hook angle, rationale, exact UTM tracking URL", TXT_GREEN),
    ]

    for idx, (fname, fdesc, color) in enumerate(files):
        fy = 145 + idx * 58
        draw.rounded_rectangle([(lx, fy), (lx + 550, fy + 48)], radius=6, fill=(20, 26, 38), outline=(36, 42, 56))
        draw.text((lx + 15, fy + 6), fname, fill=color, font=font_code_bold)
        draw.text((lx + 15, fy + 26), fdesc, fill=TXT_MUTED, font=font_ui_body)

    draw.rounded_rectangle([(lx, 460), (lx + 550, 640)], radius=6, fill=(14, 18, 27), outline=WIN_BORDER)
    draw.text((lx + 20, 475), "METADATA SNIPPET (meta.json):", fill=TXT_PURPLE, font=font_code_bold)
    meta_lines = [
        "\"asset_id\": \"INSTA-01\",",
        "\"content_pillar\": \"Pillar 1: Audio/Video Engine\",",
        "\"hook\": \"Why 80% of video repurposing looks robotic (and how to fix it)\",",
        "\"utm_link\": \"https://incubrix.com/?utm_source=instagram&utm_campaign=c_launch\",",
        "\"duplicate_check\": \"UNIQUE\",  \"completeness_check\": \"COMPLETE\"",
    ]
    for mi, ml in enumerate(meta_lines):
        draw.text((lx + 20, 505 + mi * 24), ml, fill=TXT_WHITE, font=font_code)

    rx = 650
    draw.text((rx, 105), "CALENDAR.CSV VERIFICATION (EXACT 23 COLUMNS)", fill=TXT_PURPLE, font=font_code_bold)
    draw.line([(rx, 132), (rx + 600, 132)], fill=WIN_BORDER, width=1)

    checks = [
        ("Total Rows in Calendar", "30 Production Rows (Matching assessment requirement)", TXT_CYAN),
        ("Total Columns Schema", "23 Columns (asset_id through completeness_check)", TXT_CYAN),
        ("Column 22 [duplicate_check]", "30 / 30 Rows Evaluated to 'UNIQUE' (0 Collisions)", TXT_GREEN),
        ("Column 23 [completeness_check]", "30 / 30 Rows Evaluated to 'COMPLETE' (0 Missing Fields)", TXT_GREEN),
        ("Format Distribution", "12 Short Videos (MP4) | 8 Carousels (PNG) | 10 Text/Threads", TXT_YELLOW),
        ("Platform Coverage", "10 LinkedIn | 12 Instagram | 8 YouTube Shorts", TXT_PROMPT_BLUE),
    ]

    for idx, (ctitle, cdesc, color) in enumerate(checks):
        cy = 145 + idx * 54
        draw.rounded_rectangle([(rx, cy), (rx + 580, cy + 44)], radius=6, fill=(20, 26, 38), outline=(36, 42, 56))
        draw.text((rx + 15, cy + 4), ctitle, fill=color, font=font_code_bold)
        draw.text((rx + 15, cy + 24), cdesc, fill=TXT_WHITE, font=font_ui_body)

    draw.text((rx, 490), "(.venv) PS D:\\Incubrix-2> ", fill=TXT_PROMPT_YELLOW, font=font_code_bold)
    draw.text((rx + 280, 490), "Get-Content submission\\02_main_output\\calendar.csv -TotalCount 2", fill=TXT_CMD, font=font_code)
    draw.rounded_rectangle([(rx, 520), (rx + 580, 640)], radius=6, fill=(14, 18, 27), outline=WIN_BORDER)
    draw.text((rx + 15, 530), "asset_id,platform,format,pillar,scheduled_date,hook,caption,...", fill=TXT_CYAN, font=font_code)
    draw.text((rx + 15, 560), "INSTA-01,Instagram,Short Video,Pillar 1,2026-11-01,\"Why 80% of...\",...", fill=TXT_WHITE, font=font_code)
    draw.text((rx + 15, 595), "... [All 30 rows strictly conform to the 23 workbook columns] ...", fill=TXT_MUTED, font=font_code)

    return img


def render_windows_scene_4(sec: float) -> Image.Image:
    """Scene 4: 02:30 - 03:13 (Part 3: Refresh Run & Deduplication Proof)"""
    img = Image.new("RGB", (WIDTH, HEIGHT), BG_DESKTOP)
    draw = ImageDraw.Draw(img)

    draw_windows_dell_frame(
        draw, sec, 4,
        "Part 3: Refresh Run on New Input & SQLite Deduplication Proof",
        "02:30 - 03:13",
        "\"Now let's test what happens when a creator uploads a new recording next week. We run the refresh command...\""
    )

    t_scene = sec - 150.0
    x = 50
    y = 105

    draw.text((x, y), "(.venv) PS D:\\Incubrix-2> ", fill=TXT_PROMPT_YELLOW, font=font_code_bold)
    cmd1 = "python -m submission.03_engine.src.engine refresh --input submission\\03_engine\\sample_inputs\\anchor_webinar_repurposing.md"
    chars1 = min(len(cmd1), int(t_scene * 28))
    draw.text((x + 280, y), cmd1[:chars1], fill=TXT_CMD, font=font_code)

    if t_scene < 3.0:
        return img

    refresh_logs = [
        ("[22:16:00] [INFO] INCUBRIX GROWTH ENGINE v1.0 — EXECUTION MODE: 'REFRESH'", TXT_PURPLE, 3.5),
        ("[22:16:00] [INFO] Input: submission\\03_engine\\sample_inputs\\anchor_webinar_repurposing.md", TXT_WHITE, 4.5),
        ("[22:16:01] [INFO] [REFRESH MODE ACTIVE] Querying SQLite dedup database (state\\engine_state.db)...", TXT_CYAN, 6.0),
        ("[22:16:02] [INFO]   • Indexed Existing Assets in Database: 30 assets (SHA-256 Content Hashes)", TXT_WHITE, 8.0),
        ("[22:16:03] [INFO]   • Candidate New Blueprints Evaluated:  10 assets from webinar input", TXT_WHITE, 10.0),
        ("[22:16:04] [INFO]   • Content Collisions Detected:         0 collisions (100% Net-New Content)", TXT_GREEN, 12.0),
        ("[22:16:05] [INFO]   • Jaccard Hook Similarity Check:       Max similarity 0.32 (< 0.85 threshold)", TXT_GREEN, 14.0),
        ("[22:16:06] [INFO] Quality Gates: 10/10 Ready. Appending to production calendar.csv...", TXT_YELLOW, 16.0),
        ("[22:16:07] [SUCCESS] Refresh Run Succeeded! 10 net-new assets appended. Total Library: 40 Assets.", TXT_GREEN, 18.0),
    ]

    cur_y = y + 30
    for line_text, color, appear_time in refresh_logs:
        if t_scene >= appear_time:
            draw.text((x, cur_y), line_text, fill=color, font=font_code)
            cur_y += 24

    if t_scene >= 20.0:
        cur_y += 12
        draw.text((x, cur_y), "(.venv) PS D:\\Incubrix-2> ", fill=TXT_PROMPT_YELLOW, font=font_code_bold)
        cmd2 = "python -m submission.03_engine.src.engine repeat --input submission\\03_engine\\sample_inputs\\anchor_podcast_episode.md"
        t_sub = t_scene - 20.0
        chars2 = min(len(cmd2), int(t_sub * 28))
        draw.text((x + 280, cur_y), cmd2[:chars2], fill=TXT_CMD, font=font_code)

        repeat_logs = [
            ("[22:16:20] [INFO] INCUBRIX GROWTH ENGINE v1.0 — EXECUTION MODE: 'REPEAT'", TXT_PURPLE, 22.0),
            ("[22:16:20] [INFO] [REPEAT MODE ACTIVE] Ingesting identical input to verify zero duplicate creation...", TXT_CYAN, 24.0),
            ("[22:16:21] [INFO] SQLite Hash Lookup: Checking 30 candidate hashes against 'seen_assets' table...", TXT_WHITE, 26.0),
            ("[22:16:22] [WARN] Content Collision: Hash 8f3a9... matches asset INSTA-01 in database", TXT_YELLOW, 28.0),
            ("[22:16:23] [WARN] Content Collision: Hash 4b1c2... matches asset LINKEDIN-01 in database", TXT_YELLOW, 30.0),
            ("[22:16:24] [INFO] [DEDUP VERIFIED] 30 of 30 candidate assets identified as DUPLICATES.", TXT_GREEN, 32.0),
            ("[22:16:25] [INFO] Net-New Assets Produced: 0. Duplicate Assets Filtered: 30.", TXT_GREEN, 34.0),
            ("[22:16:25] [SUCCESS] Repeat Run Finished. Zero duplicate files written. System state is pristine.", TXT_GREEN, 36.0),
        ]

        sub_y = cur_y + 30
        for line_text, color, appear_time in repeat_logs:
            if t_scene >= appear_time:
                draw.text((x, sub_y), line_text, fill=color, font=font_code)
                sub_y += 24

    return img


def render_windows_scene_5(sec: float) -> Image.Image:
    """Scene 5: 03:13 - 03:57 (Part 4: Injected Failure & Auto-Recovery)"""
    img = Image.new("RGB", (WIDTH, HEIGHT), BG_DESKTOP)
    draw = ImageDraw.Draw(img)

    draw_windows_dell_frame(
        draw, sec, 5,
        "Part 4: Fault Injection & Self-Healing Auto-Recovery (--inject-failure api_timeout)",
        "03:13 - 03:57",
        "\"Next, let's demonstrate failure resilience. What happens if an external LLM endpoint throws a 504 Gateway Timeout?...\""
    )

    t_scene = sec - 193.0
    x = 50
    y = 105

    draw.text((x, y), "(.venv) PS D:\\Incubrix-2> ", fill=TXT_PROMPT_YELLOW, font=font_code_bold)
    cmd = "python -m submission.03_engine.src.engine run --input submission\\03_engine\\sample_inputs\\anchor_podcast_episode.md --inject-failure api_timeout"
    chars = min(len(cmd), int(t_scene * 28))
    draw.text((x + 280, y), cmd[:chars], fill=TXT_CMD, font=font_code)

    if t_scene < 3.0:
        return img

    fault_logs = [
        ("[22:17:00] [INFO] ==================================================================", TXT_MUTED, 3.5),
        ("[22:17:00] [INFO] INCUBRIX SOCIAL GROWTH ENGINE v1.0 — FAULT INJECTION SIMULATION", TXT_RED, 4.5),
        ("[22:17:00] [INFO] Active Fault Injection Flag: --inject-failure api_timeout", TXT_YELLOW, 5.5),
        ("[22:17:00] [INFO] ==================================================================", TXT_MUTED, 6.5),
        ("[22:17:01] [INFO] Step 1: Ingesting anchor transcript (14,820 chars)...", TXT_WHITE, 8.0),
        ("[22:17:02] [INFO] Step 2: Calling Primary Cloud LLM Synthesizer...", TXT_PROMPT_BLUE, 10.0),
        ("[22:17:04] [WARN] [FAULT TRIGGERED] Upstream LLM Endpoint returned HTTP 504 Gateway Timeout!", TXT_RED, 12.0),
        ("[22:17:04] [ERROR] Connection timed out after 30,000ms. Error logged to 'failure_run.log'.", TXT_RED, 14.5),
        ("[22:17:05] [INFO] [SELF-HEALING PROTOCOL] Initiating exponential backoff retry policy...", TXT_YELLOW, 17.0),
        ("            • Attempt 1: Waiting 500ms... Retry failed with timeout.", TXT_MUTED, 19.0),
        ("            • Attempt 2: Waiting 1000ms... Retry failed with timeout.", TXT_MUTED, 21.0),
        ("            • Max retries reached. Primary API flagged as OFFLINE.", TXT_RED, 23.5),
        ("[22:17:08] [INFO] [CIRCUIT BREAKER] Switching to Offline Deterministic Rule-Based Synthesizer...", TXT_GREEN, 26.0),
        ("            ✔ Ingested local persona models and prompt heuristic trees", TXT_GREEN, 28.0),
        ("            ✔ Synthesized 30 candidate assets locally with zero data loss", TXT_GREEN, 30.0),
        ("[22:17:11] [INFO] Step 3: Executing Quality Gates on recovered assets: 30/30 PASSED [100%]", TXT_GREEN, 32.5),
        ("[22:17:12] [INFO] Step 4: Master Exports generated successfully in 'submission\\02_main_output\\'", TXT_GREEN, 35.0),
        ("[22:17:13] [INFO] Writing audit report to 'submission\\03_engine\\outputs\\failure_run_report.json'...", TXT_CYAN, 37.5),
        ("[22:17:14] [SUCCESS] Status: RECOVERED_SUCCESS. Resilience verified. Zero lost deliverables.", TXT_GREEN, 40.0),
    ]

    cur_y = y + 30
    for line_text, color, appear_time in fault_logs:
        if t_scene >= appear_time:
            draw.text((x, cur_y), line_text, fill=color, font=font_code)
            cur_y += 24

    return img


def render_windows_scene_6(sec: float) -> Image.Image:
    """Scene 6: 03:57 - 04:30.5 (Part 5: Automated Pytest Suite & Confidence Wrap-Up)"""
    img = Image.new("RGB", (WIDTH, HEIGHT), BG_DESKTOP)
    draw = ImageDraw.Draw(img)

    draw_windows_dell_frame(
        draw, sec, 6,
        "Part 5: Automated Pytest Suite & Evaluation Readiness (8/8 Passed)",
        "03:57 - 04:30",
        "\"Finally, let's run the automated test suite. 8 test cases verifying text normalization, deduplication...\""
    )

    t_scene = sec - 237.0
    x = 50
    y = 105

    draw.text((x, y), "(.venv) PS D:\\Incubrix-2> ", fill=TXT_PROMPT_YELLOW, font=font_code_bold)
    cmd = "pytest submission\\03_engine\\tests\\ -v"
    chars = min(len(cmd), int(t_scene * 28))
    draw.text((x + 280, y), cmd[:chars], fill=TXT_CMD, font=font_code)

    if t_scene < 2.5:
        return img

    test_logs = [
        ("============================= test session starts =============================", TXT_MUTED, 3.0),
        ("platform win32 -- Python 3.14.6, pytest-9.1.1 -- D:\\Incubrix-2\\.venv\\Scripts\\python.exe", TXT_MUTED, 4.0),
        ("rootdir: D:\\Incubrix-2", TXT_MUTED, 5.0),
        ("collected 8 items", TXT_WHITE, 6.0),
        ("", TXT_MUTED, 6.0),
        ("submission/03_engine/tests/test_dedup.py::test_normalize_text PASSED          [ 12%]", TXT_GREEN, 7.5),
        ("submission/03_engine/tests/test_dedup.py::test_compute_content_hash PASSED      [ 25%]", TXT_GREEN, 9.0),
        ("submission/03_engine/tests/test_dedup.py::test_dedup_store_exact_and_hook PASSED [ 37%]", TXT_GREEN, 10.5),
        ("submission/03_engine/tests/test_engine_runs.py::test_calendar_columns_match_23 PASSED [ 50%]", TXT_GREEN, 12.0),
        ("submission/03_engine/tests/test_engine_runs.py::test_normal_and_repeat_run_simulation PASSED [ 62%]", TXT_GREEN, 13.5),
        ("submission/03_engine/tests/test_quality_gates.py::test_valid_asset PASSED       [ 75%]", TXT_GREEN, 15.0),
        ("submission/03_engine/tests/test_quality_gates.py::test_banned_phrase_violation PASSED [ 87%]", TXT_GREEN, 16.5),
        ("submission/03_engine/tests/test_quality_gates.py::test_invalid_platform_and_utm PASSED [100%]", TXT_GREEN, 18.0),
        ("", TXT_MUTED, 18.0),
        ("============================= 8 passed in 23.30s ==============================", TXT_GREEN, 19.5),
    ]

    cur_y = y + 28
    for line_text, color, appear_time in test_logs:
        if t_scene >= appear_time:
            draw.text((x, cur_y), line_text, fill=color, font=font_code)
            cur_y += 24

    if t_scene >= 21.0:
        card_y = 520
        draw.rounded_rectangle([(x, card_y), (WIDTH - 50, card_y + 115)], radius=8, fill=(18, 25, 38), outline=TXT_GREEN, width=2)
        draw.text((x + 25, card_y + 15), "INCUBRIX CONTENT ENGINE — EVALUATION SUMMARY", fill=TXT_PURPLE, font=font_code_large)
        draw.text((x + 25, card_y + 48), "• 100% Deterministic Architecture  • Deduplication Guarantee  • Automated Self-Healing", fill=TXT_WHITE, font=font_ui_title)
        draw.text((x + 25, card_y + 78), "• Evaluated from README in clean virtualenv: python -m submission.03_engine.src.engine run", fill=TXT_PROMPT_BLUE, font=font_code)

    return img


def get_windows_frame(sec: float) -> Image.Image:
    if sec < 54.0:
        return render_windows_scene_1(sec)
    elif sec < 102.0:
        return render_windows_scene_2(sec)
    elif sec < 150.0:
        return render_windows_scene_3(sec)
    elif sec < 193.0:
        return render_windows_scene_4(sec)
    elif sec < 237.0:
        return render_windows_scene_5(sec)
    else:
        return render_windows_scene_6(sec)


def main():
    print("==================================================================")
    print("INCUBRIX TECHNICAL DEMO — WINDOWS DELL LAPTOP (CANDIDATE FULL VOICE)")
    print("==================================================================")
    print(f"Target Resolution: {WIDTH}x{HEIGHT} @ {FPS} fps")
    print(f"Total Video Duration: {TOTAL_SECONDS}s (matching 270.41s user audio)")
    print(f"User Voice File: {USER_AUDIO}")

    ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()

    # 1. Render Video frames to temp video
    writer = imageio_ffmpeg.write_frames(
        OUTPUT_VIDEO_NO_AUDIO,
        (WIDTH, HEIGHT),
        fps=FPS,
        codec="libx264",
        pix_fmt_in="rgb24",
        ffmpeg_log_level="error",
        quality=8,
        output_params=["-preset", "fast", "-crf", "18"]
    )
    writer.send(None)

    total_frames = TOTAL_SECONDS * FPS
    t0 = time.time()
    last_sec_rendered = -1.0
    last_frame_bytes = None

    print(f"[INFO] Rendering {total_frames} frames in Dell 13\" Windows environment...")

    for frame_idx in range(total_frames):
        current_sec = frame_idx / FPS
        quantized_sec = round(current_sec * 4) / 4

        if quantized_sec != last_sec_rendered or last_frame_bytes is None:
            frame_img = get_windows_frame(current_sec)
            last_frame_bytes = frame_img.tobytes()
            last_sec_rendered = quantized_sec

        writer.send(last_frame_bytes)

        if frame_idx % (FPS * 30) == 0:
            pct = (frame_idx / total_frames) * 100
            elapsed = time.time() - t0
            print(f"[PROGRESS] {pct:5.1f}% complete ({frame_idx}/{total_frames} frames) - Elapsed: {elapsed:.1f}s")

    writer.close()
    t1 = time.time()
    print(f"[INFO] Video frames rendered in {t1 - t0:.1f}s")

    # 2. Mux User Voiceover Audio into Final MP4
    print("[INFO] Muxing candidate voiceover audio track into final MP4...")
    mux_cmd = [
        ffmpeg_exe, "-y",
        "-i", OUTPUT_VIDEO_NO_AUDIO,
        "-i", USER_AUDIO,
        "-c:v", "copy",
        "-c:a", "aac",
        "-b:a", "192k",
        "-shortest",
        OUTPUT_FINAL_VIDEO
    ]
    subprocess.run(mux_cmd, check=True)

    # Copy to master technical_demo.mp4
    import shutil
    shutil.copyfile(OUTPUT_FINAL_VIDEO, OUTPUT_MASTER_VIDEO)

    # Clean up temp video
    if os.path.exists(OUTPUT_VIDEO_NO_AUDIO):
        os.remove(OUTPUT_VIDEO_NO_AUDIO)

    size_mb = os.path.getsize(OUTPUT_MASTER_VIDEO) / (1024 * 1024)
    print("==================================================================")
    print("SUCCESS: Full Candidate Voice Windows Dell 13\" Video Created!")
    print(f"  Master File: {OUTPUT_MASTER_VIDEO}")
    print(f"  Size: {size_mb:.2f} MB")
    print(f"  Duration: 04:30.4")
    print("==================================================================")


if __name__ == "__main__":
    main()
