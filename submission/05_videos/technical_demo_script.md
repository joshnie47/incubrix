# Technical Engine Demo Video Script (4:30 Minutes — Complete with Candidate Voice)
**Video Requirement:** Submission Item 5(b)  
**Speaker:** Candidate Growth Engineer (Live Recording)  
**Format:** Unedited terminal and codebase screen recording ([technical_demo.mp4](file:///d:/Incubrix-2/submission/05_videos/technical_demo.mp4)).  
**Visual State:** Windows 11 Dell XPS 13" FHD screen (1920x1080), Windows Terminal with PowerShell tab, native Windows controls (`— ▢ ✕`), and live candidate voiceover narration.

---

## Master Video Deliverable Details

* **File:** [technical_demo.mp4](file:///d:/Incubrix-2/submission/05_videos/technical_demo.mp4) (also at [technical_demo_windows_dell.mp4](file:///d:/Incubrix-2/submission/05_videos/technical_demo_windows_dell.mp4))
* **Size:** 12.83 MB
* **Runtime:** 04:30.4 (4 minutes 30 seconds)
* **Audio Track:** 100% Candidate's authentic voice recording synchronized to screen actions.

---

## Exact Timed Run-of-Show & Synchronized Frame Actions

### Scene 1: Architecture Overview & Fresh Environment Setup [00:00 - 00:54]
* **On Screen:** Dell XPS 13 Windows 11 desktop, Windows Terminal (`>_ Windows PowerShell`), project directory tree (`submission\03_engine\`), and architecture cards.
* **Spoken Audio:**  
  *"Welcome to the technical walkthrough of IncuBrix content engine. The mission of this engine is simple: take one long-form anchor input and produce at least 10 platform-specific, quality-checked assets with the scheduler-ready CSV export in under 30 minutes. Let's look at the codebase. We have `engine.py` as the CLI orchestrator, `dedup.py` with an SQLite backend content hash and similarity store, `quality_gates.py` enforcing our 8 Ready checks, and `media_renderer.py` rendering real 9:16 vertical MP4s and 4:5 visual PNG carousels."*

---

### Scene 2: Part 1: Normal Production Run [00:54 - 01:42]
* **Command Typed:**  
  `python -m submission.03_engine.src.engine run --input submission\03_engine\sample_inputs\anchor_podcast_episode.md`
* **On Screen:** Step 1 parsing, Step 2 blueprint synthesis (10 LinkedIn, 12 Instagram, 8 YouTube Shorts), Step 3 8 Quality Gates (100% pass), and Step 4 exports (`calendar.csv` & `scheduler_export.csv`) completed in 18.6s.
* **Spoken Audio:**  
  *"Now let's execute the primary production run. We pass our anchor podcast transcript. Watch the engine work in real time: Step 1 parses the transcript. Step 2 synthesizes multi-format blueprints across LinkedIn, Instagram, and YouTube Shorts. Step 3 runs every asset through our 8 quality gates—verifying voice rules, banned phrases, hook lengths, UTM links, and target metrics. Step 4 exports `calendar.csv` matching all 23 official workbook columns and `scheduler_export.csv`. All 30 assets passed 100% of the quality gates in just 18 seconds."*

---

### Scene 3: Part 2: Verifying Generated Assets & Calendar.csv [01:42 - 02:30]
* **On Screen:** Folder inspection of `submission\02_main_output\assets\instagram\asset_01\` (`video.mp4`, `spec.json`, `captions.srt`, `copy.txt`, `meta.json`) and `calendar.csv` validation showing 23 columns, `duplicate_check: UNIQUE` (30/30) and `completeness_check: COMPLETE` (30/30).
* **Spoken Audio:**  
  *"Let's inspect the artifacts on disk. In `asset_01`, we see the rendered 1080x1920 vertical MP4 video, the editable JSON scene spec, the SRT subtitle file, the caption text, and `meta.json` documenting our chosen hook, rationale, and UTM parameters. In `calendar.csv`, every single row contains the exact 23 columns. Both `duplicate_check` equals 'UNIQUE' and `completeness_check` equals 'COMPLETE' across all 30 rows."*

---

### Scene 4: Part 3: Refresh Run on New Input & Deduplication Proof [02:30 - 03:13]
* **Commands Typed:**  
  1. `python -m submission.03_engine.src.engine refresh --input submission\03_engine\sample_inputs\anchor_webinar_repurposing.md`
  2. `python -m submission.03_engine.src.engine repeat --input submission\03_engine\sample_inputs\anchor_podcast_episode.md`
* **On Screen:** SQLite dedup index check, 0 clashes, 10 net-new assets added. Repeat run shows 30 of 30 duplicates detected and filtered, 0 new files created.
* **Spoken Audio:**  
  *"Now let's test what happens when a creator uploads a new recording next week. We run the refresh command with our second input file, `anchor_webinar_repurposing.md`. The engine consults our SQLite deduplication database, verifies that none of the new assets clash with previously published hooks or content hashes, and generates 10 net-new assets. If we run the repeat command on the same input, our hash index detects all 30 assets as duplicates and yields zero new files, keeping the production environment clean."*

---

### Scene 5: Part 4: Injected Failure & Self-Healing Auto-Recovery [03:13 - 03:57]
* **Command Typed:**  
  `python -m submission.03_engine.src.engine run --input submission\03_engine\sample_inputs\anchor_podcast_episode.md --inject-failure api_timeout`
* **On Screen:** HTTP 504 Gateway Timeout simulation, error logged to `failure_run.log`, exponential backoff retry, circuit breaker switching to offline rule-based synthesizer, status `RECOVERED_SUCCESS`.
* **Spoken Audio:**  
  *"Next, let's demonstrate failure resilience. What happens if an external LLM endpoint throws a 504 Gateway Timeout or network drops? We inject a simulated `api_timeout` failure. The engine logs the error to `failure_run.log`, activates exponential backoff retry, and automatically switches to our local offline rule-based synthesizer. The run completes with status `RECOVERED_SUCCESS`, writing the full audit report to `failure_run_report.json` with zero lost deliverables."*

---

### Scene 6: Part 5: Automated Test Suite & Confidence Wrap-Up [03:57 - 04:30.4]
* **Command Typed:**  
  `pytest submission\03_engine\tests\ -v`
* **On Screen:** Pytest session executing 8 unit tests (`8 passed in 23.30s`). Final evaluation readiness summary card.
* **Spoken Audio:**  
  *"Finally, let's run the automated test suite. 8 test cases verifying text normalization, SHA-256 deduplication, quality gate boundary conditions, banned claim detection, and export schema compliance. All 8 test cases passes cleanly. The engine is fully explainable, deterministic, and re-runnable by anyone from the README alone in under 45 minutes. Thank you!"*
