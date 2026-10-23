"""
IncuBrix Real-Audience Test Analyzer
Computes preference rates, utility ratings, and benchmark comparisons
from test_kit/raw_results.csv.
"""

import csv
import json
import os


def analyze_survey_results(csv_path: str = "test_kit/raw_results.csv") -> dict:
    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"Survey results CSV not found at: {csv_path}")

    with open(csv_path, "r", encoding="utf-8") as f:
        reader = list(csv.DictReader(f))

    total_respondents = len(reader)
    if total_respondents == 0:
        return {}

    # 1. Geographic & Persona breakdown
    geos = {}
    personas = {}
    for r in reader:
        g = r["geography"]
        p = r["creator_type"]
        geos[g] = geos.get(g, 0) + 1
        personas[p] = personas.get(p, 0) + 1

    # 2. A/B Preferences
    q3_opt_a = sum(1 for r in reader if r["q3_hook_choice"] == "Option A")
    q3_opt_b = total_respondents - q3_opt_a
    q3_pref_a_pct = round((q3_opt_a / total_respondents) * 100, 1)

    q4_opt_a = sum(1 for r in reader if r["q4_subtitle_choice"] == "Option A")
    q4_opt_b = total_respondents - q4_opt_a
    q4_pref_a_pct = round((q4_opt_a / total_respondents) * 100, 1)

    q5_opt_a = sum(1 for r in reader if r["q5_format_choice"] == "Option A")
    q5_opt_b = total_respondents - q5_opt_a
    q5_pref_a_pct = round((q5_opt_a / total_respondents) * 100, 1)

    # 3. Utility ratings
    q6_ratings = [float(r["q6_repurposing_utility_rating"]) for r in reader]
    q6_avg = round(sum(q6_ratings) / len(q6_ratings), 2)

    q7_ratings = [float(r["q7_free_credits_appeal_rating"]) for r in reader]
    q7_avg = round(sum(q7_ratings) / len(q7_ratings), 2)

    # 4. Industry Benchmarks Comparison (from research/sources.md)
    # Industry benchmark for standard A/B preference: 50/50 baseline, 65% is statistically significant at p < 0.05
    # Industry benchmark for creator utility rating: 3.8 / 5.0 (Sprout Social creator SaaS average)
    benchmark_preference_pct = 65.0
    benchmark_utility_score = 3.80

    metrics = {
        "total_respondents": total_respondents,
        "personas": personas,
        "geographies": geos,
        "hook_preference": {
            "option_a_votes": q3_opt_a,
            "option_b_votes": q3_opt_b,
            "option_a_pct": q3_pref_a_pct,
            "beats_benchmark": q3_pref_a_pct > benchmark_preference_pct,
            "benchmark_pct": benchmark_preference_pct,
        },
        "karaoke_subtitles_preference": {
            "option_a_votes": q4_opt_a,
            "option_b_votes": q4_opt_b,
            "option_a_pct": q4_pref_a_pct,
            "beats_benchmark": q4_pref_a_pct > benchmark_preference_pct,
        },
        "repurposing_carousel_preference": {
            "option_a_votes": q5_opt_a,
            "option_b_votes": q5_opt_b,
            "option_a_pct": q5_pref_a_pct,
        },
        "repurposing_framework_utility_avg": q6_avg,
        "repurposing_utility_beats_benchmark": q6_avg > benchmark_utility_score,
        "free_credits_appeal_avg": q7_avg,
        "benchmark_utility_score": benchmark_utility_score,
    }

    return metrics


if __name__ == "__main__":
    results = analyze_survey_results()
    print("=== INCUBRIX REAL-AUDIENCE TEST ANALYSIS ===")
    print(json.dumps(results, indent=2))
