# Assignment

MAS664 Homework 6

## Overview

Core idea + architecture
A persistent API + online demo service that works collaboratively to build a rubric, ask for
refinements/validation, and score outputs based on the rubric. It also saves rubric data for future
evaluations. Components could include a rubric builder, a rubric refiner, a rubric database, and a
scorer/validator.

### Adjacent / Relevant Resources

https://ai.meta.com/research/publications/rubric-based-benchmarking-and-reinforcement-learning-for-advancing-llm-instruction-following/

https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents

#### Heuristics for Starting the API Server

Running the server:

source .venv/bin/activate
uvicorn main:app --reload
<!-- main corresponds to main.py, app is the variable name, so it's equivalent to from main import app -->

Test API at: http://127.0.0.1:8000/docs

#### Misc Notes

<!-- Quick rebuild: uv pip install -r requirements.txt -->
<!-- Stuck processes: lsof -ti :8000; investigate process; kill [process id] -->
