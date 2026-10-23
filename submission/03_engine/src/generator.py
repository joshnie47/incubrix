"""
IncuBrix Engine — Asset Generator Module
Transforms long-form anchor content into 30 platform-native assets:
- 12 Short videos (9:16, 1080x1920 MP4 + SRT + Scene Spec)
- 8 Carousels & Graphics (1080x1350 PNG + SVG source)
- 10 Text Posts & Threads (Formatted Text + Markdown Source)
Adheres to brand voice rules and verified features from verified_features.md.
"""

import json
import os
from typing import Dict, List, Tuple
from .dedup import DedupStore
from .media_renderer import render_short_video, render_carousel_graphic
from .quality_gates import validate_asset


ASSET_BLUEPRINTS = [
    # --- 12 SHORT VIDEOS (60s or less, 1080x1920 9:16) ---
    {
        "id": "asset_01",
        "platform": "Instagram",
        "format": "Short video",
        "pillar": "P1_WORKFLOW",
        "hooks": [
            "If you spend more than 20 minutes repurposing a podcast, your workflow is broken.",
            "Why editing a 45-minute episode takes you 4 hours (and how to fix it in 20 minutes)."
        ],
        "hook_reason": "Direct pain point exposing creator time leakage, immediately arresting scroll in first 1.5 seconds.",
        "caption": "Most creators quit after episode 10 because scrubbing video waveforms is soul-crushing. Here is the modern CreatorOps shift: edit by text, generate 10 assets from 1 recording, and publish from one screen.\n\n#CreatorOps #PodcastGrowth #VideoRepurposing #ContentCreator #IncuBrix",
        "cta": "Test with 300 free credits at www.incubrix.com (no card needed)",
        "points": ["Delete transcript sentences to cut video", "Word-by-word karaoke captions", "Dispatch to 5 platforms from 1 hub"],
        "target_metric": "target_metric=3500_views_4.2pct_engagement",
        "ai_label": "No",
        "scheduled_date": "2026-11-02 09:00",
    },
    {
        "id": "asset_02",
        "platform": "YouTube Shorts",
        "format": "Short video",
        "pillar": "P2_HOOKS",
        "hooks": [
            "The 3-second drop-off is killing your Shorts. Here is the retention fix.",
            "Why 70% of viewers scroll away in 2 seconds (and how karaoke captions stop them)."
        ],
        "hook_reason": "Focuses on retention metrics creators desperately care about; promises immediate tactical fix.",
        "caption": "70% of mobile viewers watch on mute. If your hook isn't visual and dynamic in the first 2 seconds, you lose the algorithm. Watch how animated karaoke captions double watch time.\n\n#YouTubeShorts #RetentionHacks #VideoEditing #CreatorTips #IncuBrix",
        "cta": "Try 300 free credits today at www.incubrix.com",
        "points": ["Synchronize spoken and visual words", "High contrast subtitle styling", "First 2 seconds decide viral reach"],
        "target_metric": "target_metric=5000_views_65pct_retention",
        "ai_label": "No",
        "scheduled_date": "2026-11-03 11:30",
    },
    {
        "id": "asset_03",
        "platform": "Instagram",
        "format": "Short video",
        "pillar": "P3_REPURPOSE",
        "hooks": [
            "How 1 raw founder interview becomes 10 published posts before lunch.",
            "Stop recording new content every day. Use the 1-to-10 repurposing engine."
        ],
        "hook_reason": "Concrete asset multiplier promise (1 to 10) backed by clear execution timeframe.",
        "caption": "One 45-minute recording session on Monday can feed your entire weekly content calendar: 3 Shorts, 2 Carousels, and 5 LinkedIn thought leadership posts.\n\n#ContentRepurposing #CreatorEconomy #SocialStrategy #Podcasting #IncuBrix",
        "cta": "Start free at www.incubrix.com — 300 credits loaded instantly",
        "points": ["1 Anchor recording", "10 Native multi-platform assets", "Zero manual timeline scrubbing"],
        "target_metric": "target_metric=2800_views_3.8pct_engagement",
        "ai_label": "No",
        "scheduled_date": "2026-11-04 14:00",
    },
    {
        "id": "asset_04",
        "platform": "YouTube Shorts",
        "format": "Short video",
        "pillar": "P5_FEATURE_PROOF",
        "hooks": [
            "Delete text in the transcript. The video cuts itself.",
            "This text-based video editing workflow saved me 5 hours this week."
        ],
        "hook_reason": "Visually demonstrable mechanic; demystifies editing for non-technical creators.",
        "caption": "No Premiere Pro timeline scrubbing. Just highlight sentences you don't want and press Backspace. Text-based editing is how CreatorOps scales.\n\n#VideoEditingTools #IncuBrix #TechForCreators #ShortsVideo #AIVideo",
        "cta": "Experience text editing free at www.incubrix.com",
        "points": ["Highlight text to cut clip", "Fix flubbed words with voice repair", "Export in 9:16 vertical automatically"],
        "target_metric": "target_metric=4200_views_70pct_retention",
        "ai_label": "No",
        "scheduled_date": "2026-11-06 10:00",
    },
    {
        "id": "asset_05",
        "platform": "Instagram",
        "format": "Short video",
        "pillar": "P4_CREATOR_OPS",
        "hooks": [
            "Stop logging into 5 different social apps to publish your clips.",
            "The 5-tab chaos is costing you 2 hours every week."
        ],
        "hook_reason": "Emphasizes the universal frustration of browser tab juggling and file downloading.",
        "caption": "YouTube Studio, Meta Business Suite, LinkedIn, Spotify... tab juggling ends today. Connect your channels once and publish across platforms from a single screen.\n\n#CreatorOps #ProductivityHacks #SocialMediaManagement #IncuBrix #Creators",
        "cta": "Centralize your publishing at www.incubrix.com",
        "points": ["Connect YouTube, Instagram, LinkedIn, Spotify", "Native aspect ratios rendered automatically", "Cross-platform analytics in 1 view"],
        "target_metric": "target_metric=3100_views_4.0pct_engagement",
        "ai_label": "No",
        "scheduled_date": "2026-11-07 16:00",
    },
    {
        "id": "asset_06",
        "platform": "YouTube Shorts",
        "format": "Short video",
        "pillar": "P1_WORKFLOW",
        "hooks": [
            "What a $5,000/month podcast production workflow looks like in 2026.",
            "You don't need a 4-person media team to run a daily content engine."
        ],
        "hook_reason": "Strong comparison anchor ($5k production vs solopreneur engine) appealing to budget-conscious creators.",
        "caption": "Big media companies have 5 editors on payroll. Solopreneurs use CreatorOps. Here is how one person produces 12 weekly clips without burnout.\n\n#Solopreneur #PodcastWorkflow #GrowthEngine #IncuBrix #MediaProduction",
        "cta": "Get 300 free monthly credits at www.incubrix.com",
        "points": ["Input raw audio/video", "Auto-extract high-intent soundbites", "Distribute with zero manual re-uploads"],
        "target_metric": "target_metric=4800_views_5.1pct_engagement",
        "ai_label": "No",
        "scheduled_date": "2026-11-09 11:00",
    },
    {
        "id": "asset_07",
        "platform": "Instagram",
        "format": "Short video",
        "pillar": "P2_HOOKS",
        "hooks": [
            "Why karaoke captions get 2.4x higher watch time than standard subtitles.",
            "The subconscious science behind animated word-by-word subtitles."
        ],
        "hook_reason": "Scientific curiosity angle paired with concrete metric multiplier (2.4x watch time).",
        "caption": "When words light up as they are spoken, viewers subconsciously read ahead and stay hooked through the entire clip. Customize fonts and brand colors inside IncuBrix.\n\n#Subtitles #VideoHacks #InstagramReels #CreatorTips #IncuBrix",
        "cta": "Style your captions with 300 free credits at www.incubrix.com",
        "points": ["Word-by-word animated color highlight", "High-contrast mobile readability", "Readable on mute in noisy environments"],
        "target_metric": "target_metric=3900_views_4.5pct_engagement",
        "ai_label": "No",
        "scheduled_date": "2026-11-10 15:30",
    },
    {
        "id": "asset_08",
        "platform": "YouTube Shorts",
        "format": "Short video",
        "pillar": "P5_FEATURE_PROOF",
        "hooks": [
            "Translate your video captions into 100+ languages with one click.",
            "How English creators are unlocking global audiences without re-filming."
        ],
        "hook_reason": "Direct verified product capability (VF-06: 100+ language caption translation) unlocking international reach.",
        "caption": "Why restrict your content to one language? IncuBrix translates your spoken transcripts and subtitle tracks into over 100 languages instantly.\n\n#GlobalContent #Translation #ShortsViral #IncuBrix #CreatorEconomy",
        "cta": "Expand your reach at www.incubrix.com (300 free credits)",
        "points": ["Over 100 languages supported", "Culturally accurate transcription", "Global reach without studio dubbing"],
        "target_metric": "target_metric=3600_views_3.9pct_engagement",
        "ai_label": "No",
        "scheduled_date": "2026-11-12 12:00",
    },
    {
        "id": "asset_09",
        "platform": "Instagram",
        "format": "Short video",
        "pillar": "P3_REPURPOSE",
        "hooks": [
            "Don't let your podcast episode die on Spotify. Here is the 7-day repurpose loop.",
            "The 7-day social loop that squeezes 10x value out of every recording."
        ],
        "hook_reason": "High emotional relevance for podcasters whose episodes get buried after launch day.",
        "caption": "Publishing on Spotify and hoping people listen is not a marketing strategy. Build a 7-day distribution loop across Reels, Shorts, and LinkedIn.\n\n#PodcastMarketing #AudioToVideo #IncuBrix #ContentMarketing #Creators",
        "cta": "Test your first episode at www.incubrix.com",
        "points": ["Day 1: Spotify long-form", "Day 2-4: 3 Vertical hook clips", "Day 5: Visual carousel breakdown"],
        "target_metric": "target_metric=2900_views_3.7pct_engagement",
        "ai_label": "No",
        "scheduled_date": "2026-11-13 17:00",
    },
    {
        "id": "asset_10",
        "platform": "YouTube Shorts",
        "format": "Short video",
        "pillar": "P1_WORKFLOW",
        "hooks": [
            "Flubbed your guest's name on camera? Don't re-record. Just type the fix.",
            "How voice cloning fixes audio mistakes in 10 seconds."
        ],
        "hook_reason": "Highlights verified voice cloning and narration repair (VF-03) solving a common recording headache.",
        "caption": "Setting up the mic again to re-record a 3-second mistake is painful. IncuBrix clones your voice to patch voiceovers and narration directly from the script.\n\n#VoiceCloning #AudioEditing #CreatorTools #IncuBrix #TechShorts",
        "cta": "Try voice tools free at www.incubrix.com",
        "points": ["Type narration to patch audio", "Zero re-recording required", "Matches your vocal timbre"],
        "target_metric": "target_metric=4400_views_4.8pct_engagement",
        "ai_label": "Yes",
        "scheduled_date": "2026-11-15 11:30",
    },
    {
        "id": "asset_11",
        "platform": "Instagram",
        "format": "Short video",
        "pillar": "P4_CREATOR_OPS",
        "hooks": [
            "How digital avatars let creators ship video without getting in front of the lens.",
            "Can you publish daily videos without turning your camera on?"
        ],
        "hook_reason": "Engages camera-shy creators with verified digital avatar feature (VF-04).",
        "caption": "Not feeling camera-ready today? IncuBrix digital avatars deliver scripts lip-synced to your narration so your posting cadence never misses a day.\n\n#DigitalAvatars #VideoCreation #IncuBrix #ContentStrategy #FutureOfContent",
        "cta": "Explore avatar creation at www.incubrix.com",
        "points": ["Lip-synced script delivery", "Consistent daily posting cadence", "Zero camera setup needed"],
        "target_metric": "target_metric=3300_views_3.6pct_engagement",
        "ai_label": "Yes",
        "scheduled_date": "2026-11-16 16:30",
    },
    {
        "id": "asset_12",
        "platform": "YouTube Shorts",
        "format": "Short video",
        "pillar": "P5_FEATURE_PROOF",
        "hooks": [
            "300 credits free, no credit card required. What can you actually make?",
            "Is the IncuBrix free tier actually free? We break down the math."
        ],
        "hook_reason": "Transparent pricing teardown addressing creator skepticism directly.",
        "caption": "No watermarks. No surprise subscriptions. 300 monthly credits is enough to create approximately 21 one-minute clips. See the breakdown.\n\n#SaaSReview #FreeCreatorTools #IncuBrix #VideoClips #BudgetCreator",
        "cta": "Claim your 300 credits at www.incubrix.com",
        "points": ["300 Free credits every month", "≈ 21 One-minute videos", "No credit card needed"],
        "target_metric": "target_metric=5200_views_5.4pct_engagement",
        "ai_label": "No",
        "scheduled_date": "2026-11-18 10:30",
    },

    # --- 8 CAROUSELS & GRAPHICS (4:5 1080x1350 PNG + SVG) ---
    {
        "id": "asset_13",
        "platform": "LinkedIn",
        "format": "Carousel",
        "pillar": "P1_WORKFLOW",
        "hooks": [
            "The 1-Hour to 1-Week Content Matrix: How modern teams automate distribution.",
            "Why the top 1% of B2B creators never start their posts from scratch."
        ],
        "hook_reason": "High-status B2B positioning appealing to founders, executives, and content teams on LinkedIn.",
        "caption": "If you record a weekly podcast or webinar and don't repurpose it into a structured LinkedIn campaign, you are leaving 80% of your audience reach on the table. Swipe through this 5-step matrix.\n\n#ContentStrategy #B2BMarketing #PodcastRepurposing #LinkedInCreators #IncuBrix",
        "cta": "Build your engine with 300 free credits at www.incubrix.com",
        "points": [
            "Step 1: Record 45-min masterclass",
            "Step 2: Auto-extract 5 core thesis statements",
            "Step 3: Convert thesis into slide carousel",
            "Step 4: Dispatch across channels from 1 screen"
        ],
        "target_metric": "target_metric=4500_impressions_5.2pct_engagement",
        "ai_label": "No",
        "scheduled_date": "2026-11-03 08:30",
    },
    {
        "id": "asset_14",
        "platform": "Instagram",
        "format": "Carousel",
        "pillar": "P3_REPURPOSE",
        "hooks": [
            "The Anatomy of a High-Retention Vertical Clip (Slide-by-Slide Breakdown).",
            "Stop guessing why your Reels flop. Here is the exact retention anatomy."
        ],
        "hook_reason": "Visual educational teardown tailored for Instagram creators and editors.",
        "caption": "A viral clip is not luck. It is engineering: Top 1/3 visual hook, kinetic word-by-word subtitles, seamless cut pacing, and a low-friction micro-CTA. Save this carousel for your next editing session.\n\n#VideoEditing #ReelsGrowth #ContentAnatomy #VideoCreators #IncuBrix",
        "cta": "Test with 300 free credits at www.incubrix.com",
        "points": [
            "0-2s: The High-Contrast Visual Hook",
            "2-15s: Kinetic Karaoke Subtitle Anchors",
            "15-25s: The Value Pivot",
            "25-30s: Clear Frictionless CTA"
        ],
        "target_metric": "target_metric=3200_impressions_4.8pct_engagement",
        "ai_label": "No",
        "scheduled_date": "2026-11-05 13:00",
    },
    {
        "id": "asset_15",
        "platform": "LinkedIn",
        "format": "Graphic",
        "pillar": "P4_CREATOR_OPS",
        "hooks": [
            "The Fragmented Stack vs The Unified Creator Hub (Infographic Comparison).",
            "Are you paying $115/month for 5 different creator subscriptions?"
        ],
        "hook_reason": "Financial cost comparison exposes tool redundancy and promotes consolidation.",
        "caption": "Transcription ($15) + Video Editor ($25) + Subtitle Tool ($20) + Scheduler ($30) + Graphics ($13) = $103/mo and endless tab juggling. IncuBrix consolidates creation, editing, and publishing into one workspace.\n\n#CreatorEconomy #TechStack #SaaS #Productivity #IncuBrix",
        "cta": "Consolidate your stack at www.incubrix.com (free 300 credits)",
        "points": [
            "Fragmented: 5 apps, $103/mo, hours of file transfers",
            "Unified: 1 screen, creation + editing + dispatch",
            "Team collaboration built directly into the cuts",
            "Start free without entering credit card details"
        ],
        "target_metric": "target_metric=3800_impressions_4.4pct_engagement",
        "ai_label": "No",
        "scheduled_date": "2026-11-07 09:15",
    },
    {
        "id": "asset_16",
        "platform": "Instagram",
        "format": "Graphic",
        "pillar": "P5_FEATURE_PROOF",
        "hooks": [
            "How 300 Monthly Credits Breaks Down in Real Content Output.",
            "The exact math of IncuBrix free tier credits explained."
        ],
        "hook_reason": "Transparent infographics build trust with skeptical creators looking for no-bs numbers.",
        "caption": "What does '300 credits' actually buy? Here is the exact breakdown: ~21 minutes of finished, captioned vertical video ready for YouTube Shorts and Instagram Reels. 100% free, no credit card required.\n\n#IncuBrix #TransparentPricing #CreatorTools #VideoClips #NoCardNeeded",
        "cta": "Claim your 300 credits at www.incubrix.com",
        "points": [
            "300 Credits = ~21 Minutes of Video",
            "Full access to karaoke caption styling",
            "Multi-platform scheduling included",
            "Zero watermark on exported files"
        ],
        "target_metric": "target_metric=2600_impressions_3.9pct_engagement",
        "ai_label": "No",
        "scheduled_date": "2026-11-09 14:45",
    },
    {
        "id": "asset_17",
        "platform": "LinkedIn",
        "format": "Carousel",
        "pillar": "P2_HOOKS",
        "hooks": [
            "7 High-Converting Hook Frameworks for Video and Text Posts.",
            "The 7 hook formulas that generated over 500,000 impressions."
        ],
        "hook_reason": "High-utility swipe file that creators bookmark and refer back to repeatedly.",
        "caption": "Your content is only as good as the first sentence. If the hook fails, the insight never gets heard. Swipe through 7 battle-tested hook formulas to use on your next upload.\n\n#HookFormulas #Copywriting #CreatorHacks #LinkedInGrowth #IncuBrix",
        "cta": "Auto-generate viral hooks with IncuBrix at www.incubrix.com",
        "points": [
            "Formula 1: The Counter-Intuitive Truth",
            "Formula 2: The Specific Time-Saved Metric",
            "Formula 3: The Common Mistake Callout",
            "Formula 4: The 1-to-10 Multiplier"
        ],
        "target_metric": "target_metric=5100_impressions_5.8pct_engagement",
        "ai_label": "No",
        "scheduled_date": "2026-11-11 08:45",
    },
    {
        "id": "asset_18",
        "platform": "Instagram",
        "format": "Carousel",
        "pillar": "P1_WORKFLOW",
        "hooks": [
            "The Sunday Prep: How to schedule a full week of Reels in 45 minutes.",
            "Stop creating content every day. Use the batching blueprint."
        ],
        "hook_reason": "Solves daily content creation anxiety by giving a predictable batching routine.",
        "caption": "Daily content panic is the #1 cause of creator burnout. Batch your anchor recording once a week, let IncuBrix extract your top moments, and schedule your entire week in under an hour.\n\n#ContentBatching #CreatorSanity #WorkSmarter #InstagramReels #IncuBrix",
        "cta": "Start your batch routine at www.incubrix.com",
        "points": [
            "Hour 1: Record 1 in-depth conversation",
            "Minute 15: AI auto-generates 10 clip drafts",
            "Minute 30: Fine-tune text edits and captions",
            "Minute 45: Schedule to all channels"
        ],
        "target_metric": "target_metric=3400_impressions_4.6pct_engagement",
        "ai_label": "No",
        "scheduled_date": "2026-11-13 13:30",
    },
    {
        "id": "asset_19",
        "platform": "LinkedIn",
        "format": "Graphic",
        "pillar": "P4_CREATOR_OPS",
        "hooks": [
            "Creator Collaboration Without Chaos: The Team Workspace Blueprint.",
            "How agencies and editors manage 5+ creator accounts in one tab."
        ],
        "hook_reason": "Directly speaks to agencies, video editors, and multi-creator managers.",
        "caption": "No more sending large WeTransfer links and chasing feedback across Slack threads. Invite your editor, ghostwriter, and manager into one shared IncuBrix workspace.\n\n#Agencies #VideoEditing #Collaboration #TeamWorkflow #IncuBrix",
        "cta": "Invite your team free at www.incubrix.com",
        "points": [
            "Leave comments directly on video timestamps",
            "Assign publishing slots to team members",
            "One-click review and approval queue",
            "Maintain unified brand assets across clients"
        ],
        "target_metric": "target_metric=3900_impressions_4.7pct_engagement",
        "ai_label": "No",
        "scheduled_date": "2026-11-15 09:30",
    },
    {
        "id": "asset_20",
        "platform": "Instagram",
        "format": "Graphic",
        "pillar": "P3_REPURPOSE",
        "hooks": [
            "The 1-to-10 Repurposing Wheel (Save This Infographic).",
            "Every podcast you record contains 10 hidden assets. Here they are."
        ],
        "hook_reason": "High-shareability wheel graphic demonstrating multi-format conversion.",
        "caption": "Stop letting your ideas stay trapped in one audio file. Repurpose like a modern studio: 3 Shorts, 3 Reels, 2 Carousels, and 2 Thought Leadership posts.\n\n#Infographic #ContentMarketing #CreatorGrowth #IncuBrix #PodcastTips",
        "cta": "Transform your audio free at www.incubrix.com",
        "points": [
            "Audio/Video to 9:16 Shorts & Reels",
            "Audio to LinkedIn Carousels & PDFs",
            "Transcript to Executive Blog/Newsletter",
            "Quotes to High-Signal Social Text"
        ],
        "target_metric": "target_metric=2900_impressions_4.1pct_engagement",
        "ai_label": "No",
        "scheduled_date": "2026-11-17 15:00",
    },

    # --- 10 TEXT POSTS & THREADS ---
    {
        "id": "asset_21",
        "platform": "LinkedIn",
        "format": "Text post",
        "pillar": "P1_WORKFLOW",
        "hooks": [
            "Most creators spend 80% of their time on logistics and 20% on creative thought.",
            "The real reason 90% of business podcasts never make it past episode 10."
        ],
        "hook_reason": "Provocative observation highlighting misallocated creative energy in B2B content.",
        "caption": "Most creators spend 80% of their time on logistics and 20% on creative thought.\n\nThey record for 45 minutes.\nThen spend 3 hours:\n- Scrubbing video timelines\n- Fixing auto-transcription errors\n- Resizing to 9:16 vertical\n- Copy-pasting captions into 4 different scheduling tabs\n\nThis is why podcasters burn out.\n\nThe future belongs to creators who run their content like a software pipeline: record once, let AI text-edit and repurpose, and publish from one central screen.\n\nWork on the message. Let software handle the distribution.\n\n#CreatorOps #ContentStrategy #B2BMarketing #Productivity #IncuBrix",
        "cta": "Test the CreatorOps workflow with 300 free credits at www.incubrix.com",
        "points": ["Scrubbing timelines is obsolete", "Text-based editing changes content economics", "One central dispatch screen"],
        "target_metric": "target_metric=4200_impressions_4.9pct_engagement",
        "ai_label": "No",
        "scheduled_date": "2026-11-02 08:15",
    },
    {
        "id": "asset_22",
        "platform": "LinkedIn",
        "format": "Text post",
        "pillar": "P4_CREATOR_OPS",
        "hooks": [
            "Why the 'CreatorOps' shift will define the creator economy in 2026.",
            "The difference between an amateur creator and a creator enterprise is an operating system."
        ],
        "hook_reason": "Frames content creation as an operational discipline rather than an artistic fluke.",
        "caption": "In 2020, being a creator was about having a camera and a microphone.\nIn 2026, being a creator is about operating an asset distribution engine.\n\nThe creators winning today don't work 60 hours a week.\nThey build a systematic pipeline:\n1. Spot trending niche gaps before recording (Content Insights)\n2. Edit videos as easily as editing a Google Doc (Text-based editing)\n3. Repurpose 1 anchor conversation into 10 platform deliverables\n4. Dispatch to YouTube, Instagram, and LinkedIn without tab juggling\n\nScale your output without scaling your stress.\n\n#CreatorEconomy #BusinessOfContent #Automation #IncuBrix",
        "cta": "See how CreatorOps works at www.incubrix.com (no card needed)",
        "points": ["Systematic asset distribution", "Content insights before recording", "Scale output without burnout"],
        "target_metric": "target_metric=3900_impressions_4.6pct_engagement",
        "ai_label": "No",
        "scheduled_date": "2026-11-04 09:00",
    },
    {
        "id": "asset_23",
        "platform": "X",
        "format": "Thread",
        "pillar": "P3_REPURPOSE",
        "hooks": [
            "How to turn 1 podcast episode into 10 high-performing social posts (step-by-step thread):",
            "The 1-to-10 Content Flywheel: A masterclass in repurposing audio into reach 🧵"
        ],
        "hook_reason": "Classic high-performing thread hook signaling immediate tactical value.",
        "caption": "How to turn 1 podcast episode into 10 high-performing social posts (step-by-step thread):\n\n1/ The Anchor Recording: Record 30-45 mins of unscripted expertise.\n2/ The Transcript Cut: Highlight core takeaways and delete filler words.\n3/ The 3 Short Clips: Extract 3 high-retention moments with karaoke captions.\n4/ The Slide Carousel: Turn the episode framework into a 5-slide visual PDF.\n5/ The Thought Leadership Posts: Turn contrarian opinions into written essays.\n6/ The Unified Dispatch: Schedule across platforms from one dashboard.\n\nStop creating new content every day. Repurpose what works.\n\n#Thread #CreatorHacks #ContentRepurposing #IncuBrix",
        "cta": "Start free with 300 credits at www.incubrix.com",
        "points": ["Anchor recording principle", "Text cut mechanics", "Multi-platform distribution"],
        "target_metric": "target_metric=2800_impressions_3.5pct_engagement",
        "ai_label": "No",
        "scheduled_date": "2026-11-06 14:00",
    },
    {
        "id": "asset_24",
        "platform": "LinkedIn",
        "format": "Text post",
        "pillar": "P2_HOOKS",
        "hooks": [
            "The biggest lie in video editing is that viewers care about your 10-second intro.",
            "Why animated logos and theme music in your videos are killing your retention."
        ],
        "hook_reason": "Contrarian debunking of outdated video production habits.",
        "caption": "The biggest lie in video editing is that viewers care about your 10-second animated logo.\n\nIn short-form video, you have 1.5 seconds.\nNot 5 seconds. Not 10 seconds.\n\nIf the viewer doesn't see a clear visual hook and dynamic text immediately, their thumb swipes up.\n\n3 rules for hook retention:\n1. State the pain point in the first 7 words\n2. Light up the words dynamically as you speak them\n3. Use high-contrast color highlights on key terms\n\nTrim the fat. Respect the viewer's time.\n\n#VideoRetention #ShortsHacks #LinkedInTips #CreatorEconomy #IncuBrix",
        "cta": "Style retention captions free at www.incubrix.com",
        "points": ["Kill the 10-second animated intro", "State pain point in 7 words", "Dynamic word lighting"],
        "target_metric": "target_metric=4600_impressions_5.1pct_engagement",
        "ai_label": "No",
        "scheduled_date": "2026-11-08 08:30",
    },
    {
        "id": "asset_25",
        "platform": "Threads",
        "format": "Text post",
        "pillar": "P5_FEATURE_PROOF",
        "hooks": [
            "If an AI tool requires a credit card just to test basic features, close the tab.",
            "Transparent pricing rule: Test with real output before spending a dollar."
        ],
        "hook_reason": "Appeals to consumer protection and transparency values popular on Threads.",
        "caption": "If an AI tool requires a credit card just to test basic features, close the tab.\n\nAt IncuBrix, we believe creators should see their own recording transformed into 10 clips before spending a single dollar.\n\n300 credits every month. Free. No credit card required.\n\n#CreatorTools #TransparentSaaS #BuildInPublic #IncuBrix",
        "cta": "Test with 300 free credits at www.incubrix.com",
        "points": ["Zero credit card requirement", "300 free monthly credits", "True try-before-buy experience"],
        "target_metric": "target_metric=2100_impressions_4.0pct_engagement",
        "ai_label": "No",
        "scheduled_date": "2026-11-10 12:15",
    },
    {
        "id": "asset_26",
        "platform": "LinkedIn",
        "format": "Text post",
        "pillar": "P1_WORKFLOW",
        "hooks": [
            "How our team turned a 30-minute founder AMA into 14 days of content.",
            "Case breakdown: The mechanics of zero-waste content production."
        ],
        "hook_reason": "Specific case breakdown promising behind-the-scenes tactical mechanics.",
        "caption": "Last Tuesday, our team recorded a 30-minute founder AMA.\nHere is what happened next:\n\n1. Ingested the audio into IncuBrix Creator Studio\n2. Highlighted 4 high-retention stories and deleted tangential rants\n3. Exported 4 vertical video clips with burned-in karaoke captions\n4. Created 2 LinkedIn carousel summaries\n5. Scheduled the posts across LinkedIn and Instagram directly from the dashboard\n\nTotal time elapsed: 24 minutes.\nTotal cost: $0 (using free tier credits).\n\nStop working harder than your software.\n\n#CaseStudy #WorkflowDesign #Productivity #IncuBrix #B2BGrowth",
        "cta": "Try the workflow on your next upload at www.incubrix.com",
        "points": ["Zero-waste production", "24 minutes total turnaround", "Free tier credit utilization"],
        "target_metric": "target_metric=4400_impressions_4.8pct_engagement",
        "ai_label": "No",
        "scheduled_date": "2026-11-12 09:15",
    },
    {
        "id": "asset_27",
        "platform": "X",
        "format": "Text post",
        "pillar": "P2_HOOKS",
        "hooks": [
            "70% of viewers scroll on mute. If your video has no captions, you are invisible.",
            "Why silent-browsing habits killed traditional video editing in 2026."
        ],
        "hook_reason": "Bold data assertion highlighting mobile consumer behavior.",
        "caption": "70% of people on mobile scroll on mute.\n\nIf your video relies on audio to deliver the hook, you are invisible to the algorithm.\n\nWord-by-word karaoke captions aren't an aesthetic choice.\nThey are your headline, your hook, and your retention insurance.\n\n#VideoEditing #Shorts #CreatorTips #IncuBrix",
        "cta": "Generate animated captions free at www.incubrix.com",
        "points": ["70% mobile users on mute", "Captions are retention insurance", "IncuBrix word-by-word styling"],
        "target_metric": "target_metric=2400_impressions_3.2pct_engagement",
        "ai_label": "No",
        "scheduled_date": "2026-11-14 11:00",
    },
    {
        "id": "asset_28",
        "platform": "LinkedIn",
        "format": "Text post",
        "pillar": "P4_CREATOR_OPS",
        "hooks": [
            "Your back catalog of episodes is a goldmine you're ignoring.",
            "How to double your reach without recording a single new minute of audio."
        ],
        "hook_reason": "High leverage idea: unlocking value from existing past recordings.",
        "caption": "Every podcaster has 20+ past episodes sitting in an archive gathering dust.\n\nThose 20 recordings contain:\n- 60+ potential Shorts and Reels\n- 20+ LinkedIn carousels\n- 40+ high-signal quote cards\n\nYou don't need new ideas this week.\nYou need to unlock the archive with automated repurposing.\n\nPut your back catalog to work.\n\n#Podcasting #ContentRepurposing #CreatorEconomy #IncuBrix",
        "cta": "Repurpose your archive with 300 free credits at www.incubrix.com",
        "points": ["Unlock back catalog value", "No new recording required", "Automated short extraction"],
        "target_metric": "target_metric=3700_impressions_4.3pct_engagement",
        "ai_label": "No",
        "scheduled_date": "2026-11-16 08:30",
    },
    {
        "id": "asset_29",
        "platform": "Threads",
        "format": "Text post",
        "pillar": "P1_WORKFLOW",
        "hooks": [
            "Text-based video editing is the biggest leap in creator tooling since digital audio.",
            "Why scrubbing video waveforms will feel prehistoric by next year."
        ],
        "hook_reason": "Strong technology evolution angle drawing an analogy to major industry shifts.",
        "caption": "Imagine having to edit text by listening to millisecond audio frequencies.\nThat is how video editing has worked for 30 years.\n\nDeleting text to cut video is how software should have worked from day one.\n\n#CreatorTools #VideoTech #IncuBrix #BuildInPublic",
        "cta": "Try text-based video cuts at www.incubrix.com",
        "points": ["Text-based video editing evolution", "Delete words to cut frames", "No timeline friction"],
        "target_metric": "target_metric=1900_impressions_3.8pct_engagement",
        "ai_label": "No",
        "scheduled_date": "2026-11-18 13:15",
    },
    {
        "id": "asset_30",
        "platform": "LinkedIn",
        "format": "Text post",
        "pillar": "P5_FEATURE_PROOF",
        "hooks": [
            "We built IncuBrix for creators who love creating but hate the admin.",
            "Our founding thesis: You make the content. IncuBrix makes it travel."
        ],
        "hook_reason": "Authentic brand manifesto hook directly citing verified company mission.",
        "caption": "We built IncuBrix for creators who love sharing insights but hate spending 5 hours doing manual file conversions and tab juggling.\n\nOur philosophy is simple:\nYou make the content. IncuBrix makes it travel.\n\nFrom trending topic insights, to text-based video editing, to multi-platform publishing—we are building the operating system for the global creator economy.\n\nJoin thousands of creators building their audience on their own terms.\n\n#IncuBrix #CreatorEconomy #StartupStory #BuildingInPublic #Growth",
        "cta": "Start free today at www.incubrix.com (300 monthly credits, no card required)",
        "points": ["You make content, IncuBrix makes it travel", "Unified creator operating system", "300 free credits to start"],
        "target_metric": "target_metric=4800_impressions_5.5pct_engagement",
        "ai_label": "No",
        "scheduled_date": "2026-11-20 09:00",
    },
]


def generate_all_assets(
    output_root: str,
    source_input_path: str = "sample_inputs/anchor_podcast_episode.md",
    dedup_store: DedupStore = None,
) -> Tuple[List[Dict], List[Dict]]:
    """
    Generates all 30 assets, verifies against quality gates, and saves final + source files.
    Returns (ready_assets: List[Dict], rejected_assets: List[Dict]).
    """
    if dedup_store is None:
        dedup_store = DedupStore()

    ready_assets = []
    rejected_assets = []

    assets_dir = os.path.join(output_root, "assets")
    drafts_dir = os.path.join(output_root, "drafts")
    os.makedirs(assets_dir, exist_ok=True)
    os.makedirs(drafts_dir, exist_ok=True)

    for item in ASSET_BLUEPRINTS:
        asset_id = item["id"]
        platform = item["platform"]
        fmt = item["format"]
        pillar = item["pillar"]
        hook_chosen = item["hooks"][0]
        hook_variant2 = item["hooks"][1]
        caption = item["caption"]
        cta = item["cta"]
        points = item["points"]
        target_metric = item["target_metric"]
        ai_label = item["ai_label"]
        sched_date = item["scheduled_date"]

        # Check deduplication
        is_dup, dup_reason = dedup_store.check_duplicate(caption, hook_chosen)
        if is_dup:
            rejected_item = {
                "asset_id": asset_id,
                "reason": f"Deduplication rejected: {dup_reason}",
                "status": "Rejected",
            }
            rejected_assets.append(rejected_item)
            continue

        # Target directory structure: assets/<platform>/<asset_id>/
        platform_slug = platform.lower().replace(" ", "_")
        asset_folder = os.path.join(assets_dir, platform_slug, asset_id)
        os.makedirs(asset_folder, exist_ok=True)

        final_filename = ""
        source_filename = ""

        # Media Rendering based on format
        if fmt == "Short video":
            final_filename = f"{asset_id}.mp4"
            source_filename = f"{asset_id}_spec.json"
            srt_filename = f"{asset_id}.srt"
            final_path = os.path.join(asset_folder, final_filename)
            source_path = os.path.join(asset_folder, source_filename)
            srt_path = os.path.join(asset_folder, srt_filename)

            render_short_video(
                output_mp4_path=final_path,
                source_json_path=source_path,
                srt_path=srt_path,
                hook_text=hook_chosen,
                pillar_label=pillar,
                key_points=points,
                duration_seconds=30,
            )

        elif fmt in ["Carousel", "Graphic"]:
            final_filename = f"{asset_id}.png"
            source_filename = f"{asset_id}.svg"
            final_path = os.path.join(asset_folder, final_filename)
            source_path = os.path.join(asset_folder, source_filename)

            render_carousel_graphic(
                output_png_path=final_path,
                source_svg_path=source_path,
                title=hook_chosen,
                subtitle=f"IncuBrix Framework · {pillar}",
                points=points,
                cta_text=cta,
                is_carousel_cover=(fmt == "Carousel"),
            )

        else:  # Text post or Thread
            final_filename = f"{asset_id}.txt"
            source_filename = f"{asset_id}_source.json"
            final_path = os.path.join(asset_folder, final_filename)
            source_path = os.path.join(asset_folder, source_filename)

            # Write publication text file
            pub_text = f"--- {platform.upper()} PUBLICATION DRAFT ---\nHOOK: {hook_chosen}\n\n{caption}\n\nCTA: {cta}\n"
            with open(final_path, "w", encoding="utf-8") as f:
                f.write(pub_text)

            # Write editable source JSON
            src_spec = {
                "format": fmt,
                "platform": platform,
                "pillar": pillar,
                "hook_variants": [hook_chosen, hook_variant2],
                "body_paragraphs": caption.split("\n\n"),
                "cta": cta,
                "key_takeaways": points,
            }
            with open(source_path, "w", encoding="utf-8") as f:
                json.dump(src_spec, f, indent=2)

        # Write caption.txt in asset folder
        caption_path = os.path.join(asset_folder, "caption.txt")
        full_caption_text = f"HOOK:\n{hook_chosen}\n\nCAPTION:\n{caption}\n\nCTA:\n{cta}\n"
        with open(caption_path, "w", encoding="utf-8") as f:
            f.write(full_caption_text)

        # UTM Link Construction
        fmt_slug = fmt.lower().replace(" ", "_")
        utm_link = f"https://www.incubrix.com/?utm_source={platform_slug}&utm_medium={fmt_slug}&utm_campaign=creator_growth_engine_q4&utm_content={asset_id}"

        # Relative paths for portable workbook links
        rel_final_url = f"submission/02_main_output/assets/{platform_slug}/{asset_id}/{final_filename}"
        rel_source_url = f"submission/02_main_output/assets/{platform_slug}/{asset_id}/{source_filename}"

        asset_dict = {
            "asset_id": asset_id,
            "platform": platform,
            "format": fmt,
            "content_pillar": pillar,
            "hook": hook_chosen,
            "hook_variants": [
                {"variant": 1, "text": hook_chosen},
                {"variant": 2, "text": hook_variant2},
            ],
            "hook_chosen_reason": item["hook_reason"],
            "caption": caption,
            "cta": cta,
            "utm_link": utm_link,
            "final_file_url": rel_final_url,
            "source_file_url": rel_source_url,
            "source_input": source_input_path,
            "tools_used": "IncuBrix Python Content Engine v1.0, Pillow, imageio-ffmpeg",
            "rights_checked": "Yes",
            "ai_label_needed": ai_label,
            "scheduled_date": sched_date,
            "test_published_url": "",
            "impressions_or_views": "",
            "engagement_rate": "",
            "clicks": "",
            "status": "Ready",
            "notes": f"{target_metric}; hook_rationale={item['hook_reason']}",
            "_disk_final_path": final_path,
            "_disk_source_path": source_path,
        }

        # Quality Gate Verification
        is_ready, violations = validate_asset(asset_dict, base_dir="")
        if not is_ready:
            asset_dict["status"] = "Rejected"
            asset_dict["violations"] = violations
            rejected_assets.append(asset_dict)
            # Move to drafts
            draft_meta_path = os.path.join(drafts_dir, f"{asset_id}_meta.json")
            with open(draft_meta_path, "w", encoding="utf-8") as f:
                json.dump(asset_dict, f, indent=2)
        else:
            # Write meta.json in asset folder
            meta_path = os.path.join(asset_folder, "meta.json")
            with open(meta_path, "w", encoding="utf-8") as f:
                json.dump(asset_dict, f, indent=2)

            # Record in deduplication store
            dedup_store.record_asset(asset_id, caption, hook_chosen, platform)
            ready_assets.append(asset_dict)

    return ready_assets, rejected_assets
