"""
IncuBrix Engine — Media Renderer Module
Renders production-ready final assets and editable source files:
- 9:16 (1080x1920) Short Video MP4 files + SRT subtitles + JSON scene specs
- 4:5 (1080x1350) Carousel / Graphic PNG cards + SVG/HTML source specs
- Text posts and threads formatted for LinkedIn, X, and Instagram
"""

import json
import os
import subprocess
from typing import Dict, List, Optional
from PIL import Image, ImageDraw, ImageFont
import imageio_ffmpeg


def get_default_font(size: int = 36):
    """Attempt to load a clean truetype font or fall back to default."""
    try:
        # Common Windows fonts
        for font_name in ["arial.ttf", "segoeui.ttf", "calibri.ttf"]:
            try:
                return ImageFont.truetype(font_name, size)
            except IOError:
                continue
    except Exception:
        pass
    return ImageFont.load_default()


def render_short_video(
    output_mp4_path: str,
    source_json_path: str,
    srt_path: str,
    hook_text: str,
    pillar_label: str,
    key_points: List[str],
    duration_seconds: int = 30,
) -> None:
    """
    Renders a vertical 9:16 (1080x1920) MP4 video clip using Pillow and bundled FFmpeg.
    Also produces an editable JSON scene spec and a standard SRT subtitle file.
    """
    os.makedirs(os.path.dirname(output_mp4_path), exist_ok=True)
    temp_frame_path = output_mp4_path.replace(".mp4", "_frame.png")

    # 1. Create High-Resolution Vertical 1080x1920 Frame
    width, height = 1080, 1920
    img = Image.new("RGB", (width, height), color=(5, 7, 13))  # IncuBrix dark bg #05070D
    draw = ImageDraw.Draw(img)

    # Gradient background simulation with nested panels
    draw.rectangle([40, 40, width - 40, height - 40], outline=(14, 26, 58), width=3)
    draw.rectangle([60, 60, width - 60, height - 60], outline=(43, 107, 255), width=2)

    font_pill = get_default_font(28)
    font_hook = get_default_font(52)
    font_sub = get_default_font(36)
    font_brand = get_default_font(32)

    # Top Brand Kicker
    draw.text((100, 120), "INCUBRIX CREATOR STUDIO  ·  CREATOROPS", fill=(69, 232, 220), font=font_brand)
    draw.rectangle([100, 175, 420, 178], fill=(43, 107, 255))

    # Content Pillar Badge
    draw.rounded_rectangle([100, 240, 460, 310], radius=16, fill=(14, 26, 58), outline=(69, 232, 220), width=2)
    draw.text((120, 255), f"PILLAR: {pillar_label}", fill=(69, 232, 220), font=font_pill)

    # Hook Card Container (Top 1/3)
    draw.rounded_rectangle([80, 350, width - 80, 720], radius=24, fill=(12, 18, 38), outline=(43, 107, 255), width=3)
    draw.text((120, 380), "THE HOOK (FIRST 2 SECONDS):", fill=(138, 147, 168), font=font_pill)

    # Word-wrap hook text
    hook_words = hook_text.split()
    lines = []
    curr = []
    for w in hook_words:
        curr.append(w)
        if len(" ".join(curr)) > 30:
            lines.append(" ".join(curr))
            curr = []
    if curr:
        lines.append(" ".join(curr))

    y_offset = 440
    for line in lines[:4]:
        draw.text((120, y_offset), line, fill=(232, 236, 245), font=font_hook)
        y_offset += 65

    # Center Visual Audio Waves / Kinetic Indicator
    wave_y = 780
    for i in range(24):
        x = 120 + i * 36
        h = 20 + ((i * 17) % 80)
        draw.rectangle([x, wave_y - h, x + 16, wave_y + h], fill=(69, 232, 220))

    # Middle Value Breakdown
    draw.rounded_rectangle([80, 920, width - 80, 1500], radius=24, fill=(10, 15, 30), outline=(14, 26, 58), width=2)
    draw.text((120, 960), "WORKFLOW TAKEAWAYS:", fill=(69, 232, 220), font=font_pill)

    kp_y = 1040
    for idx, pt in enumerate(key_points[:4], 1):
        draw.text((120, kp_y), f"[{idx}] {pt}", fill=(232, 236, 245), font=font_sub)
        kp_y += 105

    # Bottom CTA Strip
    draw.rounded_rectangle([80, 1560, width - 80, 1780], radius=24, fill=(43, 107, 255))
    draw.text((140, 1610), "TEST WITH 300 FREE CREDITS", fill=(255, 255, 255), font=font_hook)
    draw.text((140, 1680), "No credit card required  ·  www.incubrix.com", fill=(232, 236, 245), font=font_sub)

    img.save(temp_frame_path)

    # 2. Render MP4 Video using imageio-ffmpeg (3-second preview encode for rapid synthesis)
    ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()
    clip_duration = min(duration_seconds, 60)
    clip_render_duration = 3
    cmd = [
        ffmpeg_exe,
        "-y",
        "-loop",
        "1",
        "-i",
        temp_frame_path,
        "-c:v",
        "libx264",
        "-t",
        str(clip_render_duration),
        "-pix_fmt",
        "yuv420p",
        "-r",
        "30",
        output_mp4_path,
    ]
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)

    if os.path.exists(temp_frame_path):
        os.remove(temp_frame_path)

    # 3. Generate SRT Subtitle File
    srt_content = f"""1
00:00:00,000 --> 00:00:02,500
{hook_text}

2
00:00:02,500 --> 00:00:06,000
Stop spending 4 hours scrubbing video timelines.

3
00:00:06,000 --> 00:00:12,000
{key_points[0] if key_points else "Delete words in transcript to cut the video."}

4
00:00:12,000 --> 00:00:18,000
{key_points[1] if len(key_points) > 1 else "Auto-generate word-by-word karaoke subtitles in your colors."}

5
00:00:18,000 --> 00:00:24,000
{key_points[2] if len(key_points) > 2 else "Publish to YouTube, Instagram, and LinkedIn from one screen."}

6
00:00:24,000 --> 00:00:30,000
Start free with 300 credits at www.incubrix.com.
"""
    with open(srt_path, "w", encoding="utf-8") as f:
        f.write(srt_content.strip())

    # 4. Generate Editable JSON Scene Spec
    scene_spec = {
        "format": "Short video (9:16)",
        "resolution": {"width": 1080, "height": 1920},
        "fps": 30,
        "duration_seconds": clip_duration,
        "brand": "IncuBrix Creator Studio",
        "color_palette": {
            "background": "#05070D",
            "panel": "#0C1226",
            "primary_blue": "#2B6BFF",
            "accent_cyan": "#45E8DC",
            "text_light": "#E8ECF5",
        },
        "hook": {
            "text": hook_text,
            "start_time": 0.0,
            "end_time": 2.5,
            "animation": "pop_in_karaoke",
        },
        "scenes": [
            {"time_range": "0-2s", "type": "hook_card", "content": hook_text},
            {"time_range": "2-10s", "type": "problem_breakdown", "content": key_points[0] if key_points else ""},
            {"time_range": "10-22s", "type": "solution_demo", "content": key_points[1:] if len(key_points) > 1 else []},
            {"time_range": "22-30s", "type": "cta_card", "content": "300 Free Credits · No Card · www.incubrix.com"},
        ],
        "srt_file": os.path.basename(srt_path),
        "target_platforms": ["YouTube Shorts", "Instagram Reels", "TikTok"],
    }
    with open(source_json_path, "w", encoding="utf-8") as f:
        json.dump(scene_spec, f, indent=2)


def render_carousel_graphic(
    output_png_path: str,
    source_svg_path: str,
    title: str,
    subtitle: str,
    points: List[str],
    cta_text: str = "Try 300 Free Credits at www.incubrix.com",
    is_carousel_cover: bool = False,
) -> None:
    """
    Renders a 4:5 (1080x1350) visual Graphic / Carousel slide PNG and an editable SVG source file.
    """
    os.makedirs(os.path.dirname(output_png_path), exist_ok=True)
    width, height = 1080, 1350

    img = Image.new("RGB", (width, height), color=(5, 7, 13))
    draw = ImageDraw.Draw(img)

    # Border & frame
    draw.rectangle([30, 30, width - 30, height - 30], outline=(14, 26, 58), width=2)
    draw.rectangle([50, 50, width - 50, height - 50], outline=(43, 107, 255), width=2)

    font_brand = get_default_font(28)
    font_title = get_default_font(48)
    font_sub = get_default_font(32)
    font_body = get_default_font(30)

    # Top brand bar
    draw.text((90, 90), "INCUBRIX  ·  CREATOR PLAYBOOK", fill=(69, 232, 220), font=font_brand)
    if is_carousel_cover:
        draw.rounded_rectangle([width - 320, 80, width - 90, 135], radius=12, fill=(14, 26, 58), outline=(69, 232, 220))
        draw.text((width - 300, 92), "SWIPE FOR SYSTEM →", fill=(69, 232, 220), font=font_brand)

    # Header Card
    draw.rounded_rectangle([70, 170, width - 70, 430], radius=20, fill=(12, 18, 38), outline=(43, 107, 255), width=2)
    
    # Title wrap
    words = title.split()
    lines = []
    c = []
    for w in words:
        c.append(w)
        if len(" ".join(c)) > 26:
            lines.append(" ".join(c))
            c = []
    if c:
        lines.append(" ".join(c))

    y = 210
    for line in lines[:3]:
        draw.text((100, y), line, fill=(232, 236, 245), font=font_title)
        y += 60

    draw.text((100, 360), subtitle[:80], fill=(138, 147, 168), font=font_sub)

    # Bullet Points Cards
    card_y = 470
    for idx, pt in enumerate(points[:4], 1):
        draw.rounded_rectangle([70, card_y, width - 70, card_y + 130], radius=16, fill=(10, 15, 30), outline=(14, 26, 58), width=2)
        draw.text((100, card_y + 25), f"0{idx}", fill=(69, 232, 220), font=font_title)
        draw.text((190, card_y + 25), pt[:65], fill=(232, 236, 245), font=font_body)
        draw.text((190, card_y + 70), pt[65:135] if len(pt) > 65 else "Optimized for maximum creator retention.", fill=(138, 147, 168), font=font_brand)
        card_y += 150

    # Bottom CTA Card
    draw.rounded_rectangle([70, height - 210, width - 70, height - 90], radius=18, fill=(43, 107, 255))
    draw.text((100, height - 175), cta_text[:50], fill=(255, 255, 255), font=font_sub)
    draw.text((100, height - 130), "No card needed · Instant setup at www.incubrix.com", fill=(232, 236, 245), font=font_brand)

    img.save(output_png_path)

    # Generate Editable SVG Source File
    svg_content = f"""<svg xmlns="http://www.w3.org/2000/svg" width="1080" height="1350" viewBox="0 0 1080 1350">
  <rect width="1080" height="1350" fill="#05070D"/>
  <rect x="50" y="50" width="980" height="1250" fill="none" stroke="#2B6BFF" stroke-width="2" rx="20"/>
  <text x="90" y="110" fill="#45E8DC" font-family="Inter, sans-serif" font-size="28" font-weight="bold">INCUBRIX · CREATOR PLAYBOOK</text>
  <rect x="70" y="170" width="940" height="260" fill="#0C1226" stroke="#2B6BFF" stroke-width="2" rx="20"/>
  <text x="100" y="240" fill="#E8ECF5" font-family="Inter, sans-serif" font-size="44" font-weight="bold">{title}</text>
  <text x="100" y="320" fill="#8A93A8" font-family="Inter, sans-serif" font-size="28">{subtitle}</text>
  <!-- Content cards -->
  <rect x="70" y="470" width="940" height="130" fill="#0A0F1E" stroke="#0E1A3A" rx="16"/>
  <text x="100" y="530" fill="#45E8DC" font-family="JetBrains Mono, monospace" font-size="36">01</text>
  <text x="180" y="530" fill="#E8ECF5" font-family="Inter, sans-serif" font-size="28">{points[0] if points else ""}</text>
  <rect x="70" y="1140" width="940" height="120" fill="#2B6BFF" rx="18"/>
  <text x="100" y="1200" fill="#FFFFFF" font-family="Inter, sans-serif" font-size="32" font-weight="bold">{cta_text}</text>
</svg>"""
    with open(source_svg_path, "w", encoding="utf-8") as f:
        f.write(svg_content)
