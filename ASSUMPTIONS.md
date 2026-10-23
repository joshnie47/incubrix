# ASSUMPTIONS & WORKING CONVENTIONS
**Assessment:** IncuBrix 2027 Growth Engineer Role — Option 2: Social Media Marketing and Content Engine  
**Date:** October 2026  
**Status:** In Progress / Step 0:00–0:20 Setup Complete

---

## 1. Audience & Platform Assumptions
- **Target Audience:** Creators (podcasters, YouTubers, expert-led creators, newsletter writers) and their operational teams (video editors, thumbnail designers, repurposing assistants, small agency operators).
- **Target Geographies:** English-speaking primary creator economies — United States, Canada, United Kingdom, Ireland, Australia, New Zealand, Singapore.
- **Selected Platforms (3 Primary Channels):**
  1. **LinkedIn:** B2B creator economy, agency owners, business podcasters, monetization and workflow engineering.
  2. **Instagram:** Short-form visual carousels, Reels/Shorts, workflow tips, creator lifestyle, editing process breakdown.
  3. **YouTube Shorts:** High-intent search and discovery for creators looking for tutorials, AI tools, video editing workflows, and time-saving automation.
  *(Complementary test channels noted: X / Threads for quick text hooks and creator discussions).*

## 2. Product Claim & Verification Boundaries
- **Rule:** Only features observed directly or evidenced through verified documentation / UI walkthroughs are claimed as active IncuBrix features in `research/verified_features.md`.
- **Feature Neutral / Educational Core:** If product access is pending or specific features are unconfirmed, content focuses on high-utility creator education (workflow optimization, audio-to-video repurposing mechanics, title/hook science, multi-platform publishing cadence) rather than fabricating unsubstantiated software claims.

## 3. Real-Audience Test (20-Person Preference Test)
- **Synthetic Data Directive:** Per user explicit instruction, the 20-person creator preference test will be modeled with realistic synthetic creator personas (representing podcasters, YouTube creators, and video editors across US/UK/Canada/SG).
- **Survey Design:** 6–8 asset A/B comparisons, 1–5 usefulness scale, open feedback question, GDPR/DPDP consent disclosure clearly indicating this is an independent evaluation.
- **Reporting:** Fully disclosed as synthetic benchmark validation in `DISCLOSURES.md`, `test_kit/report.md`, and the submission workbook.

## 4. Automation & Engine Architecture
- **Input:** Single long-form anchor content (podcast transcript, blog markdown, or webinar recording script).
- **Output:** Multi-platform platform-native assets (10+ per run, targeting 30 Ready assets total across short video scripts/renders, visual carousels, and text posts).
- **Deduplication:** SHA-256 content hashing + normalized title/hook similarity store in SQLite/JSON.
- **Quality Gates:** 8-point automated gate (voice rules, banned claims, length/aspect-ratio, hook presence, UTM link format, target metric, rights verification, AI disclosure flag).

## 5. UTM Tracking Scheme
- **Base Domain:** `https://www.incubrix.com`
- **Format:** `https://www.incubrix.com/?utm_source={platform}&utm_medium={format}&utm_campaign=creator_growth_engine_q4&utm_content={asset_id}`
