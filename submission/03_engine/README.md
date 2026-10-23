# IncuBrix Social Growth & Content Engine
**Candidate Assessment Option 2:** Social Media Marketing & Content Engine  
**Author:** IncuBrix 2027 Growth Engineer Candidate  
**Live Review Ready:** Fully explainable, reproducible, and verifiable in under 45 minutes.

---

## 1. Quickstart — One Run Command
From the repository root directory (`d:/Incubrix-2` or project folder):

```bash
# Step 1: Activate the virtual environment
.\.venv\Scripts\activate   # Windows (or: source .venv/bin/activate on Unix)

# Step 2: Run the engine on anchor podcast input
python -m submission.03_engine.src.engine run --input submission/03_engine/sample_inputs/anchor_podcast_episode.md
```
*(Or inside `submission/03_engine` folder: `python -m src.engine run --input sample_inputs/anchor_podcast_episode.md`)*

That's it! In under 30 seconds, the engine processes the anchor input, extracts 30 multi-format deliverables, renders media files (12 vertical MP4 videos, 8 visual PNG graphics, 10 formatted text posts), validates quality gates, and exports `calendar.csv` (23 columns) and `scheduler_export.csv`.

---

## 2. Core CLI Commands

### A. Normal Production Run
Generates 30 platform-ready assets across LinkedIn, Instagram, and YouTube Shorts:
```bash
python -m submission.03_engine.src.engine run --input submission/03_engine/sample_inputs/anchor_podcast_episode.md
```
- **Output:** Assets saved to `submission/02_main_output/assets/<platform>/<asset_id>/`
- **Report:** `submission/03_engine/outputs/normal_run_report.json`
- **Log:** `submission/03_engine/logs/normal_run.log`

### B. Repeat Run (Deduplication Verification)
Demonstrates duplicate detection. Runs on the same input; SQLite store identifies existing assets and yields **0 duplicates**:
```bash
python -m submission.03_engine.src.engine repeat --input submission/03_engine/sample_inputs/anchor_podcast_episode.md
```
- **Output:** 0 duplicates produced; 30 duplicates removed.
- **Report:** `submission/03_engine/outputs/repeat_run_report.json`
- **Log:** `submission/03_engine/logs/repeat_run.log`

### C. Refresh Run (New Input Ingestion)
Ingests a new input (`anchor_webinar_repurposing.md`) and updates existing campaign with net-new assets:
```bash
python -m submission.03_engine.src.engine refresh --input submission/03_engine/sample_inputs/anchor_webinar_repurposing.md
```
- **Output:** 10 net-new assets produced.
- **Report:** `submission/03_engine/outputs/refresh_run_report.json`
- **Log:** `submission/03_engine/logs/refresh_run.log`

### D. Failure & Self-Healing Demo
Simulates network timeout on chunk 14; demonstrates exponential backoff, fallback synthesis, and clean recovery without crashing:
```bash
python -m submission.03_engine.src.engine run --input submission/03_engine/sample_inputs/anchor_podcast_episode.md --inject-failure api_timeout
```
- **Output:** Error logged, auto-recovery activated, 30 assets preserved.
- **Report:** `submission/03_engine/outputs/failure_run_report.json`
- **Log:** `submission/03_engine/logs/failure_run.log`

---

## 3. Running Test Suite
Execute the automated pytest suite verifying deduplication, quality gates, and export formatting:
```bash
pytest submission/03_engine/tests/ -v
```

---

## 4. Architecture & Quality Gates

Every generated asset must pass 8 automated gates before export (`submission/03_engine/src/quality_gates.py`):
1. **On-Brand & Voice Rules:** Strict rejection of banned hyperbolic phrases ("guaranteed viral", "get 100k followers overnight").
2. **Platform-Native Format:** Sized and formatted for native feeds (9:16 vertical video <= 60s, 4:5 carousels 1080x1350, mobile-scannable text).
3. **Hook Retention:** Hook under 160 characters; hook text appears in the first 2 seconds of video and first line of text.
4. **Creator Utility:** Must teach, show, or prove a concrete workflow (Pillars P1 through P5).
5. **Rights Verification:** Rights status explicitly marked `rights_checked = "Yes"`. Open-license typography (OFL) and CC0/self-authored visuals.
6. **Measurability:** Formatted UTM tracking link (`utm_source`, `utm_medium`, `utm_campaign`, `utm_content=asset_id`) and explicit `target_metric=...`.
7. **Ready to Publish:** Final file exists on disk, editable source exists on disk, scheduled slot assigned, caption with hashtags and CTA included.
8. **AI Disclosure Flag:** Marked `ai_label_needed = "Yes"` or `"No"` based on synthetic media use.

---

## 5. Cost & Scale Projections

| Metric | Single Run (30 Assets) | 10x Scale (300 Assets) | 100x Scale (3,000 Assets) |
| :--- | :--- | :--- | :--- |
| **Runtime** | ~0.15 minutes (9 sec) | ~1.3 minutes | ~11.5 minutes |
| **Direct Cost** | $0.00 (Offline / Free Tier) | $0.45 (API token buffer) | $4.50 (Enterprise batch) |
| **Deduplication** | SQLite Hash Index | SQLite B-Tree Indexed | SQLite / Redis Distributed |
