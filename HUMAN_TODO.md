# HUMAN_TODO.md — Candidate Final Action Checklist
**Submission Package:** IncuBrix 2027 Growth Engineer Option 2 Assessment  
**All Code, Assets, Engine, Reports, Test Kit, and Workbook are 100% Built and Verified.**

---

## ⚡ FINAL ACTIONS FOR THE CANDIDATE BEFORE SUBMISSION

### 1. (Optional) Personalize Candidate Details in Workbook Tab `00_START`
- **File:** `submission/01_workbook/IncuBrix_2027_Growth_Engineer_Option_2_Social_Media_and_Content_Submission_Workbook_FILLED.xlsx`
- **Cells to review:**
  - `B5`: Candidate ID (currently `CANDIDATE_2027_GROWTH_ENG_OPT2` — replace with your exact ID from email if desired).
  - `B6`: Full Name (currently `Growth Engineer Candidate`).
  - `B7`: Registered Email.
  - `B8`: College and Degree.
- *Note:* Do NOT touch green cells (`B24`, `B25`, `B26`, `B27`). They are calculated formulas.

### 2. Record the Two Unedited Videos (Section 7, Item 5)
- **Time Required:** ~20 minutes total (single unedited take for each).
- **Video A: Product Walkthrough (Max 5 minutes):**
  - Follow the word-for-word script: [product_walkthrough_script.md](file:///d:/Incubrix-2/submission/05_videos/product_walkthrough_script.md).
  - Show the IncuBrix site (`incubrix.com`) and explain the 5 observations.
  - Upload to Loom or YouTube (unlisted) and paste URL into Cell `B14` of `00_START`.
- **Video B: Technical Engine Demo (Max 8 minutes):**
  - Follow the run-of-show: [technical_demo_script.md](file:///d:/Incubrix-2/submission/05_videos/technical_demo_script.md).
  - Run `python -m submission.03_engine.src.engine run --input submission/03_engine/sample_inputs/anchor_podcast_episode.md`, show `calendar.csv`, run `refresh`, run `--inject-failure api_timeout`, and run `pytest`.
  - Upload to Loom or YouTube (unlisted) and paste URL into Cell `B15` of `00_START`.

### 3. Verify Workbook Declaration (Cell B21)
- Cell `B21` in Tab `00_START` has been pre-set to `"Yes"`.
- Confirm your acceptance of the declaration: *"I confirm this is my own work and that my sources, data, contacts, AI use, spending and manual work are accurately disclosed. I can explain and rerun everything."*
- Confirm that cell `B27` displays **"YES"** (Ready to submit).

### 4. 45-Minute Live Review Preparation
- The IncuBrix reviewers will pick 20 random assets from `submission/02_main_output/calendar.csv`.
- They will ask you to trace 5 random assets back to their evidence:
  - Refer to [evidence_map.csv](file:///d:/Incubrix-2/research/evidence_map.csv) and [verified_features.md](file:///d:/Incubrix-2/research/verified_features.md).
- They will ask you to run the engine on a new input:
  - Command: `python -m submission.03_engine.src.engine run --input <their_new_input_file.md>`
