from fastapi import FastAPI
from pydantic import BaseModel

import llm

app = FastAPI(title="Rubric Builder & Scorer")


class GenerateRubricRequest(BaseModel):
    prompt: str


class DimensionIn(BaseModel):
    name: str
    description: str
    scale: str = "1=poor, 5=excellent"


class ScoreRequest(BaseModel):
    input_text: str
    dimensions: list[DimensionIn]


@app.post("/api/generate-rubric")
def api_generate_rubric(body: GenerateRubricRequest):
    dimensions = llm.generate_rubric(body.prompt)
    return {"rubric": dimensions}


@app.post("/api/score")
def api_score(body: ScoreRequest):
    dims = [d.model_dump() for d in body.dimensions]
    scores = llm.score_input(body.input_text, dims)
    aggregate = round(sum(s["score"] for s in scores) / len(scores), 2)
    return {"aggregate_score": aggregate, "scores": scores}
