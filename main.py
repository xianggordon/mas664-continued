from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

import llm
import storage

app = FastAPI(title="Rubric Builder & Scorer")
templates = Jinja2Templates(directory="templates")

BASE_URL = "https://mas664-continued-production.up.railway.app"


@app.get("/", response_class=HTMLResponse)
def landing_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={"base_url": BASE_URL},
    )


# ── Request / Response Models ────────────────────────────────────────────────

class GenerateRubricRequest(BaseModel):
    prompt: str


class DimensionIn(BaseModel):
    name: str
    description: str


class RefineRubricRequest(BaseModel):
    rubric: list[DimensionIn]


class ScoreRequest(BaseModel):
    input_text: str
    rubric: list[DimensionIn]


class SaveRubricRequest(BaseModel):
    name: str
    rubric: list[DimensionIn]


# ── Endpoints ────────────────────────────────────────────────────────────────

@app.post("/api/generate-rubric")
def api_generate_rubric(body: GenerateRubricRequest):
    rubric = llm.generate_rubric(body.prompt)
    return {"rubric": rubric}


@app.post("/api/refine-rubric")
def api_refine_rubric(body: RefineRubricRequest):
    """Accept user-edited dimensions and return them as the canonical rubric.

    No LLM call — the user has already made their edits client-side.
    This endpoint validates the shape and serves as the explicit refine
    step in the generate → refine → score flow.
    """
    rubric = [d.model_dump() for d in body.rubric]
    return {"rubric": rubric}


@app.post("/api/score")
def api_score(body: ScoreRequest):
    dims = [d.model_dump() for d in body.rubric]
    scores = llm.score_input(body.input_text, dims)
    aggregate = round(sum(int(s["score"]) for s in scores) / len(scores), 2)
    return {"aggregate_score": aggregate, "scores": scores}


# ── Persistence Endpoints ────────────────────────────────────────────────────

@app.post("/api/rubrics")
def api_save_rubric(body: SaveRubricRequest):
    rubric = [d.model_dump() for d in body.rubric]
    record = storage.save_rubric(body.name, rubric)
    return record


@app.get("/api/rubrics")
def api_list_rubrics():
    return {"rubrics": storage.list_rubrics()}


@app.get("/api/rubrics/{rubric_id}")
def api_get_rubric(rubric_id: str):
    record = storage.get_rubric(rubric_id)
    if record is None:
        raise HTTPException(status_code=404, detail="Rubric not found")
    return record


@app.delete("/api/rubrics/{rubric_id}")
def api_delete_rubric(rubric_id: str):
    if not storage.delete_rubric(rubric_id):
        raise HTTPException(status_code=404, detail="Rubric not found")
    return {"deleted": True}
