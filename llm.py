import json
import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
MODEL = "gpt-5.4-mini"


def generate_rubric(prompt: str) -> list[dict]:
    """Given a prompt/text, return 5 scoring dimensions as a list of dicts."""
    response = client.chat.completions.create(
        model=MODEL,
        response_format={"type": "json_object"},
        messages=[
            {
                "role": "system",
                "content": (
                    "You are an expert evaluator. Given a piece of text or a prompt, "
                    "generate exactly 5 scoring dimensions for evaluating it. "
                    "Each dimension should be specific and relevant to the content. "
                    "Respond with JSON in this exact shape:\n"
                    '{"rubric": [{"name": "...", "description": "...", "scale": "1=poor, 5=excellent"}, ...]}'
                ),
            },
            {"role": "user", "content": f"Generate a rubric for evaluating this:\n\n{prompt}"},
        ],
    )
    data = json.loads(response.choices[0].message.content)
    return data["rubric"]


def score_input(input_text: str, dimensions: list[dict]) -> list[dict]:
    """Score input_text against each dimension. Returns list of {dimension_name, score, rationale}."""
    dims_str = "\n".join(
        f"{i+1}. {d['name']}: {d['description']} (scale: {d['scale']})"
        for i, d in enumerate(dimensions)
    )
    response = client.chat.completions.create(
        model=MODEL,
        response_format={"type": "json_object"},
        messages=[
            {
                "role": "system",
                "content": (
                    "You are an expert evaluator. Score the given text against each rubric dimension. "
                    "For each dimension provide an integer score (1-5) and a one-sentence rationale. "
                    "Respond with JSON in this exact shape:\n"
                    '{"scores": [{"dimension_name": "...", "score": 3, "rationale": "..."}, ...]}'
                ),
            },
            {
                "role": "user",
                "content": (
                    f"Text to evaluate:\n\n{input_text}\n\n"
                    f"Rubric dimensions:\n{dims_str}"
                ),
            },
        ],
    )
    data = json.loads(response.choices[0].message.content)
    return data["scores"]
