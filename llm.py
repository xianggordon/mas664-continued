"""
llm.py — LLM service layer for rubric generation and scoring.

All OpenAI API calls live here, keeping the FastAPI layer (main.py) free of
LLM-specific logic. Every function follows the same pattern:
  1. Build a system prompt that constrains the output to a specific JSON shape.
  2. Build a user message with the relevant content.
  3. Call the Chat Completions API with response_format=json_object to
     guarantee parseable JSON.
  4. Parse the response and return a plain Python data structure.
"""

import json
import os
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables from .env (expects OPENAI_API_KEY)
load_dotenv()

# Initialise the OpenAI client once at module level so all functions share it.
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Model used for all LLM calls. Change this value to switch models globally.
MODEL = "gpt-5.4-mini"


def generate_rubric(prompt: str) -> list[dict]:
    """Generate exactly 5 scoring dimensions for evaluating the given prompt.

    Returns a list of dicts with just "name" and "description" — no scale.
    The scale is a system-level concern handled by score_input (fixed 1-5).
    """
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
                    '{"rubric": [{"name": "...", "description": "..."}, ...]}'
                ),
            },
            {"role": "user", "content": f"Generate a rubric for evaluating this:\n\n{prompt}"},
        ],
    )

    data = json.loads(response.choices[0].message.content)
    return data["rubric"]


def score_input(input_text: str, dimensions: list[dict]) -> list[dict]:
    """Score a piece of text against each rubric dimension on a fixed 1-5 scale.

    Returns a list of dicts: [{"name": ..., "rationale": ..., "score": 1-5}, ...].
    """
    dims_str = "\n".join(
        f"{i+1}. {d['name']}: {d['description']}"
        for i, d in enumerate(dimensions)
    )

    response = client.chat.completions.create(
        model=MODEL,
        response_format={"type": "json_object"},
        messages=[
            {
                "role": "system",
                "content": (
                    "You are an expert evaluator. Score the given text against each rubric dimension "
                    "on a scale of 1 to 5 (1=poor, 5=excellent). "
                    "For each dimension, provide a one-sentence rationale and then an integer score. "
                    "Respond with JSON in this exact shape:\n"
                    '{"scores": [{"name": "...", "rationale": "...", "score": 1}, ...]}'
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
