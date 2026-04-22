"""
experiments.py — Experiments exploring LLM evaluation behavior.

1. Model comparison: same prompt across different models
2. Scoring consistency: same text + rubric scored multiple times
3. Rubric sensitivity: multiple rubric generations from the same prompt
"""

import json
import llm

# PROMPT = (
#     "Building language models can be profitable, but margins depend heavily on scale and "
#     "distribution. Companies like OpenAI generate revenue through API access and subscriptions, "
#     "while open-source competitors pressure pricing. Training costs run into hundreds of millions, "
#     "requiring massive capital investment upfront. However, inference costs are declining and "
#     "enterprise demand for custom models is growing. The most viable path to profitability is "
#     "through platform effects — embedding models into products with existing distribution."
# )

PROMPT = (
    "Generate evaluations to assess how good an investment memo paper is"
)

FIXED_RUBRIC = [
    {"name": "Clarity", "description": "How clearly the idea is expressed"},
    {"name": "Depth", "description": "How thoroughly the topic is explored"},
    {"name": "Accuracy", "description": "Factual correctness of the content"},
    {"name": "Relevance", "description": "How relevant the content is to the topic"},
    {"name": "Conciseness", "description": "How efficiently the point is made"},
]

def experiment_rubric_sensitivity(n_runs=5):
    """Generate rubrics N times from the same prompt, then score with each."""
    print("\n" + "=" * 60)
    print(f"EXPERIMENT 1: Rubric Sensitivity ({n_runs} rubric variants)")
    print("=" * 60)

    aggregates = []

    for run in range(n_runs):
        rubric = llm.generate_rubric(PROMPT)

        print(f"\n  Variant {run + 1} dimensions:")
        for i, d in enumerate(rubric, 1):
            print(f"    {i}. {d['name']}")

    #     scores = llm.score_input(PROMPT, rubric)
    #     aggregate = round(sum(int(s["score"]) for s in scores) / len(scores), 2)
    #     aggregates.append(aggregate)

    #     print(f"  Aggregate score: {aggregate}")

    # print(f"\n--- Summary ---")
    # mean_agg = round(sum(aggregates) / len(aggregates), 2)
    # spread = round(max(aggregates) - min(aggregates), 2)
    # print(f"  Aggregates: {aggregates}")
    # print(f"  Mean: {mean_agg}, Spread: {spread}")

def experiment_model_comparison():
    """Compare rubric generation across different models."""
    models = ["gpt-5.4", "gpt-5.4-mini", "gpt-5.4-nano"]

    print("\n" + "=" * 60)
    print("EXPERIMENT 2: Model Comparison")
    print("=" * 60)

    for model in models:
        print(f"\n--- Model: {model} ---")

        # Generate rubric
        rubric = llm.generate_rubric(PROMPT, model=model)
        print(f"  Generated rubric:")
        for i, d in enumerate(rubric, 1):
            print(f"    {i}. {d['name']}: {d['description']}")

        # # Score with the same fixed rubric for fair comparison
        # scores = llm.score_input(PROMPT, FIXED_RUBRIC, model=model)
        # aggregate = round(sum(int(s["score"]) for s in scores) / len(scores), 2)
        # print(f"  Scores (fixed rubric):")
        # for s in scores:
        #     print(f"    {s['name']}: {s['rationale']} — Score: {s['score']}/5")
        # print(f"  Aggregate: {aggregate}")


def experiment_scoring_consistency(n_runs=5):
    """Score the same text + rubric N times and measure variance."""
    print("\n" + "=" * 60)
    print(f"EXPERIMENT 3: Scoring Consistency ({n_runs} runs)")
    print("=" * 60)

    all_scores = []  # list of per-run score dicts

    for run in range(n_runs):
        scores = llm.score_input(PROMPT, FIXED_RUBRIC)
        run_scores = {s["name"]: int(s["score"]) for s in scores}
        aggregate = round(sum(run_scores.values()) / len(run_scores), 2)
        all_scores.append(run_scores)

        print(f"\n  Run {run + 1}: {run_scores}  (aggregate: {aggregate})")

    # Compute per-dimension stats
    print(f"\n--- Summary ---")
    for dim in FIXED_RUBRIC:
        name = dim["name"]
        values = [run[name] for run in all_scores]
        mean = round(sum(values) / len(values), 2)
        spread = max(values) - min(values)
        print(f"  {name}: mean={mean}, min={min(values)}, max={max(values)}, spread={spread}")


if __name__ == "__main__":
    print("\n" + "=" * 60)
    print(f"PROMPT: {PROMPT}")
    print("=" * 60)
    experiment_rubric_sensitivity()
    experiment_model_comparison()
    experiment_scoring_consistency()
