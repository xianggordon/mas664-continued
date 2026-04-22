#!/bin/bash
# Demo curl commands matching test_service.py
# Usage: bash demo_curl.sh
# Requires: server running on localhost:8000

BASE_URL="http://127.0.0.1:8000"

echo "=== 1. Generate Rubric ==="
curl -s -X POST "$BASE_URL/api/generate-rubric" \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Is building language models a profitable business?"}' \
  | python3 -m json.tool

echo ""
echo "=== 2. Score (hardcoded rubric) ==="
curl -s -X POST "$BASE_URL/api/score" \
  -H "Content-Type: application/json" \
  -d '{
    "input_text": "Climate change is a pressing issue caused by greenhouse gas emissions.",
    "rubric": [
      {"name": "Clarity", "description": "How clearly the idea is expressed", "scale": "1=poor, 5=excellent"},
      {"name": "Depth", "description": "How thoroughly the topic is explored", "scale": "1=poor, 5=excellent"},
      {"name": "Accuracy", "description": "Factual correctness of the content", "scale": "1=poor, 5=excellent"},
      {"name": "Relevance", "description": "How relevant the content is to the topic", "scale": "1=poor, 5=excellent"},
      {"name": "Conciseness", "description": "How efficiently the point is made", "scale": "1=poor, 5=excellent"}
    ]
  }' | python3 -m json.tool

echo ""
echo "=== 3. Full Flow: Generate Rubric then Score ==="
INPUT_TEXT="Building language models can be profitable, but margins depend heavily on scale and distribution. Companies like OpenAI generate revenue through API access and subscriptions, while open-source competitors pressure pricing. Training costs run into hundreds of millions, requiring massive capital investment upfront. However, inference costs are declining and enterprise demand for custom models is growing. The most viable path to profitability is through platform effects — embedding models into products with existing distribution."

echo "--- Step 1: Generate rubric ---"
RUBRIC=$(curl -s -X POST "$BASE_URL/api/generate-rubric" \
  -H "Content-Type: application/json" \
  -d "{\"prompt\": \"$INPUT_TEXT\"}")
echo "$RUBRIC" | python3 -m json.tool

echo ""
echo "--- Step 2: Score using generated rubric ---"
RUBRIC_ARRAY=$(echo "$RUBRIC" | python3 -c "import sys,json; print(json.dumps(json.load(sys.stdin)['rubric']))")
curl -s -X POST "$BASE_URL/api/score" \
  -H "Content-Type: application/json" \
  -d "{\"input_text\": \"$INPUT_TEXT\", \"rubric\": $RUBRIC_ARRAY}" \
  | python3 -m json.tool
