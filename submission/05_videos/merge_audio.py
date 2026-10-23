"""
IncuBrix Growth Engine — Audio & Video Muxer Utility
Easily merges your recorded voiceover audio file with `technical_demo.mp4`.

Usage:
  .venv\\Scripts\\python.exe submission/05_videos/merge_audio.py <path_to_your_audio_file>

Supported audio formats: .mp3, .wav, .m4a, .aac, .ogg, .flac

Example:
  .venv\\Scripts\\python.exe submission/05_videos/merge_audio.py my_voiceover.mp3
"""

import os
import sys
import subprocess
import imageio_ffmpeg


def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    video_path = os.path.join(base_dir, "technical_demo.mp4")
    output_path = os.path.join(base_dir, "technical_demo_final.mp4")

    if not os.path.exists(video_path):
        print(f"[ERROR] Base video not found at: {video_path}")
        sys.exit(1)

    audio_path = None
    if len(sys.argv) > 1:
        audio_path = sys.argv[1]
    else:
        # Auto-detect common audio files placed in submission/05_videos/
        for candidate in ["voiceover.mp3", "audio.mp3", "audio.wav", "voiceover.m4a", "technical_demo_audio.mp3", "audio.m4a"]:
            full_c = os.path.join(base_dir, candidate)
            if os.path.exists(full_c):
                audio_path = full_c
                break

    if not audio_path or not os.path.exists(audio_path):
        print("\n==================================================================")
        print("INCUBRIX AUDIO MERGER — USAGE INSTRUCTIONS")
        print("==================================================================")
        print("Please provide the path to your recorded voiceover file.")
        print("\nCommand:")
        print("  .venv\\Scripts\\python.exe submission/05_videos/merge_audio.py <your_recording.mp3>")
        print("\nOr drop your audio file into 'submission/05_videos/' named as 'audio.mp3' and rerun:")
        print("  .venv\\Scripts\\python.exe submission/05_videos/merge_audio.py")
        print("==================================================================\n")
        sys.exit(1)

    print(f"[INFO] Merging Video & Voiceover Audio...")
    print(f"  • Video:  {video_path}")
    print(f"  • Audio:  {audio_path}")
    print(f"  • Output: {output_path}")

    ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()

    cmd = [
        ffmpeg_exe, "-y",
        "-i", video_path,
        "-i", audio_path,
        "-c:v", "copy",
        "-c:a", "aac",
        "-b:a", "192k",
        "-shortest",
        output_path
    ]

    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        print(f"[ERROR] ffmpeg merging failed:\n{res.stderr}")
        sys.exit(res.returncode)

    size_mb = os.path.getsize(output_path) / (1024 * 1024)
    print("\n==================================================================")
    print("✔ SUCCESS: Final Technical Demo Video with Voiceover Created!")
    print(f"  File: {output_path}")
    print(f"  Size: {size_mb:.2f} MB")
    print("==================================================================")
    print("You can now upload 'technical_demo_final.mp4' directly to Loom, Google Drive,")
    print("or YouTube unlisted, and paste the link into 'submission/05_videos/video_links.md'")
    print("and the submission workbook!")


if __name__ == "__main__":
    main()
