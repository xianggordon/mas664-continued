#!/bin/bash
# Demo curl commands for Railway deployment
# Usage: bash demo_curl_railway.sh

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

echo ""
echo "=== 2. Score (hardcoded rubric) ==="
curl -s -X POST "$BASE_URL/api/score" \
  -H "Content-Type: application/json" \
  -d '{
    "input_text": "Climate change is a pressing issue caused by greenhouse gas emissions.",
    "rubric": [
      {"name": "Clarity", "description": "How clearly the idea is expressed"},
      {"name": "Depth", "description": "How thoroughly the topic is explored"},
      {"name": "Accuracy", "description": "Factual correctness of the content"},
      {"name": "Relevance", "description": "How relevant the content is to the topic"},
      {"name": "Conciseness", "description": "How efficiently the point is made"}
    ]
  }' | python3 -m json.tool

echo ""
echo "=== 3. Refine Rubric ==="
curl -s -X POST "$BASE_URL/api/refine-rubric" \
  -H "Content-Type: application/json" \
  -d '{
    "rubric": [
      {"name": "Clarity", "description": "How clearly the idea is expressed"},
      {"name": "Depth", "description": "How thoroughly the topic is explored"},
      {"name": "Accuracy", "description": "Factual correctness of the content"},
      {"name": "Creativity", "description": "Originality and novelty of the argument"},
      {"name": "Evidence", "description": "Quality and relevance of supporting evidence"}
    ]
  }' | python3 -m json.tool

echo ""
echo "=== 4. Persistence CRUD ==="

echo "--- Save rubric ---"
SAVED=$(curl -s -X POST "$BASE_URL/api/rubrics" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Test Rubric",
    "rubric": [
      {"name": "Clarity", "description": "How clearly the idea is expressed"},
      {"name": "Depth", "description": "How thoroughly the topic is explored"}
    ]
  }')
echo "$SAVED" | python3 -m json.tool
RUBRIC_ID=$(echo "$SAVED" | python3 -c "import sys,json; print(json.load(sys.stdin)['id'])")

echo ""
echo "--- List rubrics ---"
curl -s "$BASE_URL/api/rubrics" | python3 -m json.tool

echo ""
echo "--- Get rubric ---"
curl -s "$BASE_URL/api/rubrics/$RUBRIC_ID" | python3 -m json.tool

echo ""
echo "--- Delete rubric ---"
curl -s -X DELETE "$BASE_URL/api/rubrics/$RUBRIC_ID" | python3 -m json.tool

echo ""
echo "--- Verify 404 after delete ---"
curl -s "$BASE_URL/api/rubrics/$RUBRIC_ID" | python3 -m json.tool

echo ""
echo "=== 5. Full Flow: Generate -> Refine -> Score ==="
INPUT_TEXT="Building language models can be profitable, but margins depend heavily on scale and distribution. Companies like OpenAI generate revenue through API access and subscriptions, while open-source competitors pressure pricing. Training costs run into hundreds of millions, requiring massive capital investment upfront. However, inference costs are declining and enterprise demand for custom models is growing. The most viable path to profitability is through platform effects — embedding models into products with existing distribution."

echo "--- Step 1: Generate rubric ---"
RUBRIC=$(curl -s -X POST "$BASE_URL/api/generate-rubric" \
  -H "Content-Type: application/json" \
  -d "{\"prompt\": \"$INPUT_TEXT\"}")
echo "$RUBRIC" | python3 -m json.tool

echo ""
echo "--- Step 2: Refine — swap last dimension ---"
RUBRIC_ARRAY=$(echo "$RUBRIC" | python3 -c "
import sys, json
rubric = json.load(sys.stdin)['rubric']
rubric[4] = {'name': 'Originality', 'description': 'Novelty of the analysis and arguments presented'}
print(json.dumps(rubric))
")
REFINED=$(curl -s -X POST "$BASE_URL/api/refine-rubric" \
  -H "Content-Type: application/json" \
  -d "{\"rubric\": $RUBRIC_ARRAY}")
echo "$REFINED" | python3 -m json.tool
REFINED_ARRAY=$(echo "$REFINED" | python3 -c "import sys,json; print(json.dumps(json.load(sys.stdin)['rubric']))")

echo ""
echo "--- Step 3: Score using refined rubric ---"
curl -s -X POST "$BASE_URL/api/score" \
  -H "Content-Type: application/json" \
  -d "{\"input_text\": \"$INPUT_TEXT\", \"rubric\": $REFINED_ARRAY}" \
  | python3 -m json.tool
