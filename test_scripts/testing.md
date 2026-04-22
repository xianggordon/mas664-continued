#### Heuristics for Starting the API Server

Running the server:

uv run uvicorn main:app --reload
<!-- main corresponds to main.py, app is the variable name, so it's equivalent to from main import app -->

Test API at: http://127.0.0.1:8000/docs

Test script: uv run python test_service.py

#### Curl Commands for Testing Locally



#### Misc Notes

<!-- Quick rebuild: uv pip install -r requirements.txt -->

<!-- Stuck processes: lsof -ti :8000; investigate process; kill [process id] -->

<!-- Running as a traditional .venv

source .venv/bin/activate
pip install -r requirements.txt
python test_service.py

 -->

 #### Terminal Tests

<!--

BASE_URL="https://mas664-continued-production.up.railway.app"

echo "=== 1. Generate Rubric ==="
GENERATED=$(curl -s -X POST "$BASE_URL/api/generate-rubric" \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Is building language models a profitable business?"}')
echo "$GENERATED" | python3 -m json.tool

echo ""
echo "--- Save generated rubric ---"
GENERATED_RUBRIC=$(echo "$GENERATED" | python3 -c "import sys,json; print(json.dumps(json.load(sys.stdin)['rubric']))")
SAVE_RESULT=$(curl -s -X POST "$BASE_URL/api/rubrics" \
  -H "Content-Type: application/json" \
  -d "{\"name\": \"Generated: LLM Profitability\", \"rubric\": $GENERATED_RUBRIC}")
echo "$SAVE_RESULT" | python3 -m json.tool


echo "=== Generate Rubric ==="
GENERATED=$(curl -s -X POST "$BASE_URL/api/generate-rubric" \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Generate a rubric to evaluate output from an improv agent that creates text for entertainment"}')
echo "$GENERATED" | python3 -m json.tool

echo ""
echo "--- Save generated rubric ---"
GENERATED_RUBRIC=$(echo "$GENERATED" | python3 -c "import sys,json; print(json.dumps(json.load(sys.stdin)['rubric']))")
SAVE_RESULT=$(curl -s -X POST "$BASE_URL/api/rubrics" \
  -H "Content-Type: application/json" \
  -d "{\"name\": \"Generated: Improv Agent Rubric\", \"rubric\": $GENERATED_RUBRIC}")
echo "$SAVE_RESULT" | python3 -m json.tool

echo "--- Save rubric ---"
SAVED=$(curl -s -X POST "$BASE_URL/api/rubrics" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Generic Custom Rubric",
    "rubric": [
      {"name": "Custom Rubric Dimension 1", "description": "Test Description 1"},
      {"name": "Custom Rubric Dimension 2", "description": "Test Description 2"},
      {"name": "Custom Rubric Dimension 3", "description": "Test Description 3"}
    ]
  }')

echo "--- List rubrics ---"
curl -s "$BASE_URL/api/rubrics" | python3 -m json.tool
 -->