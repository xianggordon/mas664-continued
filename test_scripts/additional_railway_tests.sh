echo "=== 1. Generate Rubric ==="
GENERATED=$(curl -s -X POST "$BASE_URL/api/generate-rubric" \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Generate a rubric to assess call center agents"}')
echo "$GENERATED" | python3 -m json.tool