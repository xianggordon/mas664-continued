from fastapi.testclient import TestClient
from main import app
import storage
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
    print(f"  Input: 'Is building language models a profitable business?'")

    print("  Raw:")
    print(json.dumps(data, indent=2))

    print("  ---")
    for i, d in enumerate(data["rubric"], 1):
        print(f"  {i}. {d['name']}: {d['description']}")


def test_score():
    response = client.post("/api/score", json={
        "input_text": "Climate change is a pressing issue caused by greenhouse gas emissions.",
        "rubric": [
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

    print("\n=== Score ===")
    print(f"  Input: 'Climate change is a pressing issue caused by greenhouse gas emissions.'")

    print("  Raw:")
    print(json.dumps(data, indent=2))

    print("  ---")
    for s in data["scores"]:
        print(f"  {s['name']}: {s['rationale']} — Score: {s['score']}/5")
    print(f"\n  Aggregate: {data['aggregate_score']}")


def test_refine_rubric():
    # User-edited dimensions — refine is a passthrough that validates shape
    response = client.post("/api/refine-rubric", json={
        "rubric": [
            {"name": "Clarity", "description": "How clearly the idea is expressed"},
            {"name": "Depth", "description": "How thoroughly the topic is explored"},
            {"name": "Accuracy", "description": "Factual correctness of the content"},
            {"name": "Creativity", "description": "Originality and novelty of the argument"},
            {"name": "Evidence", "description": "Quality and relevance of supporting evidence"},
        ]
    })
    assert response.status_code == 200
    data = response.json()
    assert "rubric" in data
    assert len(data["rubric"]) == 5

    print("\n=== Refine Rubric ===")
    for i, d in enumerate(data["rubric"], 1):
        print(f"  {i}. {d['name']}: {d['description']}")


def test_persistence_crud():
    # Use a temp storage file to avoid polluting real data
    from pathlib import Path
    original_path = storage.STORAGE_PATH
    storage.STORAGE_PATH = Path("test_rubrics.json")

    try:
        rubric = [
            {"name": "Clarity", "description": "How clearly the idea is expressed"},
            {"name": "Depth", "description": "How thoroughly the topic is explored"},
        ]

        # Save
        save_response = client.post("/api/rubrics", json={
            "name": "Test Rubric",
            "rubric": rubric,
        })
        assert save_response.status_code == 200
        saved = save_response.json()
        assert saved["name"] == "Test Rubric"
        assert "id" in saved
        rubric_id = saved["id"]

        print("\n=== Persistence CRUD ===")
        print(f"  Saved: {saved['name']} (id: {rubric_id})")

        # List
        list_response = client.get("/api/rubrics")
        assert list_response.status_code == 200
        rubrics = list_response.json()["rubrics"]
        assert any(r["id"] == rubric_id for r in rubrics)
        print(f"  List: {len(rubrics)} rubric(s) found")

        # Get
        get_response = client.get(f"/api/rubrics/{rubric_id}")
        assert get_response.status_code == 200
        assert get_response.json()["id"] == rubric_id
        print(f"  Get: found rubric '{get_response.json()['name']}'")

        # Delete
        del_response = client.delete(f"/api/rubrics/{rubric_id}")
        assert del_response.status_code == 200
        assert del_response.json()["deleted"] is True
        print(f"  Delete: success")

        # Verify 404 after delete
        get_response = client.get(f"/api/rubrics/{rubric_id}")
        assert get_response.status_code == 404
        print(f"  Get after delete: 404 (correct)")

    finally:
        # Clean up temp file and restore original path
        if storage.STORAGE_PATH.exists():
            storage.STORAGE_PATH.unlink()
        storage.STORAGE_PATH = original_path


def test_full_flow():
    prompt = (
        "Building language models can be profitable, but margins depend heavily on scale and "
        "distribution. Companies like OpenAI generate revenue through API access and subscriptions, "
        "while open-source competitors pressure pricing. Training costs run into hundreds of millions, "
        "requiring massive capital investment upfront. However, inference costs are declining and "
        "enterprise demand for custom models is growing. The most viable path to profitability is "
        "through platform effects — embedding models into products with existing distribution."
    )

    input_text = prompt

    # Step 1: Generate rubric
    rubric_response = client.post("/api/generate-rubric", json={"prompt": prompt})
    assert rubric_response.status_code == 200
    rubric = rubric_response.json()["rubric"]
    assert len(rubric) == 5

    print("\n=== Full Flow: Generate Rubric ===")
    print(f"  Prompt: '{prompt[:80]}...'")
    for i, d in enumerate(rubric, 1):
        print(f"  {i}. {d['name']}: {d['description']}")

    # Step 2: Refine — swap one dimension
    rubric[4] = {"name": "Originality", "description": "Novelty of the analysis and arguments presented"}
    refine_response = client.post("/api/refine-rubric", json={"rubric": rubric})
    assert refine_response.status_code == 200
    rubric = refine_response.json()["rubric"]

    print(f"\n=== Full Flow: Refined Rubric ===")
    for i, d in enumerate(rubric, 1):
        print(f"  {i}. {d['name']}: {d['description']}")

    # Step 3: Score using the refined rubric
    score_response = client.post("/api/score", json={
        "input_text": input_text,
        "rubric": rubric,
    })
    assert score_response.status_code == 200
    data = score_response.json()
    assert "aggregate_score" in data
    assert len(data["scores"]) == 5

    print(f"\n=== Full Flow: Score ===")
    for s in data["scores"]:
        print(f"  {s['name']}: {s['rationale']} — Score: {s['score']}/5")
    print(f"\n  Aggregate: {data['aggregate_score']}")


if __name__ == "__main__":
    test_generate_rubric()
    test_score()
    test_refine_rubric()
    test_persistence_crud()
    test_full_flow()
