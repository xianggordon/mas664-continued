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
        "rubric": [
            {"name": "Clarity", "description": "How clearly the idea is expressed", "scale": "1=poor, 5=excellent"},
            {"name": "Depth", "description": "How thoroughly the topic is explored", "scale": "1=poor, 5=excellent"},
            {"name": "Accuracy", "description": "Factual correctness of the content", "scale": "1=poor, 5=excellent"},
            {"name": "Relevance", "description": "How relevant the content is to the topic", "scale": "1=poor, 5=excellent"},
            {"name": "Conciseness", "description": "How efficiently the point is made", "scale": "1=poor, 5=excellent"},
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
        print(f"  {s['name']}: {s['score']} — {s['rationale']}")
    print(f"\n  Aggregate: {data['aggregate_score']}")


def test_full_flow():
    
    # prompt = "Is building language models a profitable business?"
    
    # The system appears to work better on longer outputs.
    prompt = (
        "Building language models can be profitable, but margins depend heavily on scale and "
        "distribution. Companies like OpenAI generate revenue through API access and subscriptions, "
        "while open-source competitors pressure pricing. Training costs run into hundreds of millions, "
        "requiring massive capital investment upfront. However, inference costs are declining and "
        "enterprise demand for custom models is growing. The most viable path to profitability is "
        "through platform effects — embedding models into products with existing distribution."
    ) 

    # necessary for scoring
    input_text = prompt 
    


    # Step 1: Generate rubric
    rubric_response = client.post("/api/generate-rubric", json={"prompt": prompt})
    assert rubric_response.status_code == 200
    rubric = rubric_response.json()["rubric"]
    assert len(rubric) == 5

    print("\n=== Full Flow: Generate Rubric ===")
    print(f"  Prompt: '{prompt}'")
    for i, d in enumerate(rubric, 1):
        print(f"  {i}. {d['name']}: {d['description']} (scale: {d['scale']})")

    # Step 2: Score using the generated rubric
    score_response = client.post("/api/score", json={
        "input_text": input_text,
        "rubric": rubric,
    })
    assert score_response.status_code == 200
    data = score_response.json()
    assert "aggregate_score" in data
    assert len(data["scores"]) == 5

    # used to find a scale for print output (haven't looked through this one closely)
    scale_lookup = {d["name"]: d["scale"] for d in rubric}

    print(f"\n=== Full Flow: Score ===")
    print(f"  Input: '{prompt}'")
    for s in data["scores"]:
        scale = scale_lookup.get(s["name"], "N/A")
        print(f"  {s['name']}: {s['score']} (scale: {scale}) — {s['rationale']}")
    print(f"\n  Aggregate: {data['aggregate_score']}")


if __name__ == "__main__":
    test_generate_rubric()
    test_score()
    test_full_flow()
