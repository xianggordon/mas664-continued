from fastapi.testclient import TestClient
from main import app
import json

client = TestClient(app)


def test_generate_rubric():
    response = client.post("/api/generate-rubric", json={
        "prompt": "Is building language models a profitable business?"
    })
    assert response.status_code == 200
    data = response.json()
    assert "rubric" in data
    assert len(data["rubric"]) == 5

    print("\n=== Generate Rubric ===")
    print(f"  Input:    'Is building language models a profitable business?'")
    print(f"  Type:     {type(data)}")
    
    print("  Raw:")
    print(json.dumps(data, indent=2))

    print("  ---")
    for i, d in enumerate(data["rubric"], 1):
        print(f"  {i}. {d['name']}: {d['description']}")


def test_score():
    response = client.post("/api/score", json={
        "input_text": "Climate change is a pressing issue caused by greenhouse gas emissions.",
        "dimensions": [
            {"name": "Clarity", "description": "How clearly the idea is expressed"},
            {"name": "Depth", "description": "How thoroughly the topic is explored"},
            {"name": "Accuracy", "description": "Factual correctness of the content"},
            {"name": "Relevance", "description": "How relevant the content is to the topic"},
            {"name": "Conciseness", "description": "How efficiently the point is made"},
        ]
    })
    assert response.status_code == 200
    data = response.json()
    assert "aggregate_score" in data
    assert len(data["scores"]) == 5

    print("\n=== Score Input ===")
    print(f"  Input:    'Climate change is a pressing issue caused by greenhouse gas emissions.'")
    print(f"  Type:     {type(data)}")

    print("  Raw:")
    print(json.dumps(data, indent=2))

    print("  ---")
    for s in data["scores"]:
        print(f"  {s['dimension_name']}: {s['score']}/5 — {s['rationale']}")
    print(f"\n  Aggregate: {data['aggregate_score']}/5")


if __name__ == "__main__":
    test_generate_rubric()
    test_score()
