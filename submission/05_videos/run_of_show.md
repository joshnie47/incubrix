# Video Run-of-Show Checklist & Recording Guide
**Document:** `submission/05_videos/run_of_show.md`  
**Assessment Requirement:** Submission Item 5 (Two Unedited Videos)

---

## 📹 Video A: Product Walkthrough (Max 5 Minutes)
- **Tool Recommendation:** Loom / OBS Studio / QuickTime Screen Recording (Single unedited take).
- **Target Duration:** 4:30 – 4:50 (Never exceed 5:00).
- **Setup:**
  - Browser tabs open in order:
    1. `https://www.incubrix.com/` (Home page)
    2. `https://www.incubrix.com/how-it-works.html` (Workflows & Capabilities)
    3. `https://www.incubrix.com/pricing.html` (Pricing & 300 Free Credits)
- **Checklist:**
  - [ ] State candidate name and role: Growth Engineer Option 2 assessment.
  - [ ] Show tagline and problem: Repurposing paradox & 4 hours wasted scrubbing timelines.
  - [ ] Show Observation 1: Content Insights (trending topics & competitor gaps).
  - [ ] Show Observation 2: Text-based editing (delete transcript text to cut video).
  - [ ] Show Observation 3: Word-by-word karaoke captions & 100% preference result.
  - [ ] Show Observation 4: Unified publishing hub & team collaboration workspace.
  - [ ] Show Observation 5: 300 free monthly credits with zero credit card required.
- **Upload:** Save recording to Google Drive / Loom / YouTube (unlisted) and paste URL into `submission/05_videos/video_links.md` and Workbook Tab `00_START` (Cell B14).

---

## 💻 Video B: Technical Engine Demo (4 Minutes — Ready-to-Merge)
- **Status:** Visual video pre-rendered at [technical_demo.mp4](file:///d:/Incubrix-2/submission/05_videos/technical_demo.mp4) (1080p Full HD, 30 fps, 4:00 runtime).
- **How to Add Your Voice:**
  1. Open [technical_demo.mp4](file:///d:/Incubrix-2/submission/05_videos/technical_demo.mp4) and play it while reading [technical_demo_script.md](file:///d:/Incubrix-2/submission/05_videos/technical_demo_script.md).
  2. Follow the on-screen **"🎙️ VOICE OVER CUE"** yellow prompts at the bottom of the video.
  3. Save your audio (e.g. `voiceover.mp3`) and merge with one command:
     ```powershell
     .venv\Scripts\python.exe submission/05_videos/merge_audio.py voiceover.mp3
     ```
  4. Upload `technical_demo_final.mp4` (or `technical_demo.mp4`) to Loom, Google Drive, or YouTube (unlisted).
  5. Paste the link into `submission/05_videos/video_links.md` and Workbook Tab `00_START` (Cell B15).
