import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_engine_health_endpoint():
    res = client.get("/api/v1/stats-engine/health")
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "healthy"
    assert data["domain_active"] == "price_statistics"

def test_stats_calculate_endpoint():
    payload = {
        "operation": "price_relative",
        "inputs": {"current_price": 75.0, "base_price": 50.0}
    }
    res = client.post("/api/v1/stats/calculate", json=payload)
    assert res.status_code == 200
    data = res.json()
    assert data["operation"] == "price_relative"
    assert data["result"] == 150.0
    assert data["unit"] == "percent"

def test_stats_calculate_invalid_input():
    payload = {
        "operation": "price_relative",
        "inputs": {"current_price": 75.0, "base_price": 0.0}
    }
    res = client.post("/api/v1/stats/calculate", json=payload)
    assert res.status_code == 400
    err = res.json()
    assert "detail" in err

def test_competencies_endpoints():
    res = client.get("/api/v1/competencies")
    assert res.status_code == 200
    comps = res.json()
    assert len(comps) >= 1
    price_comp = next((c for c in comps if c["id"] == "price_statistics"), None)
    assert price_comp is not None
    assert len(price_comp["skills"]) >= 8

    # Detail endpoint
    res_detail = client.get("/api/v1/competencies/price_statistics")
    assert res_detail.status_code == 200
    assert res_detail.json()["id"] == "price_statistics"

def test_question_generate_and_submit_lifecycle():
    # 1. Request question generation
    gen_payload = {
        "skill_id": "price.price_relative",
        "difficulty": "basic",
        "seed": 4321
    }
    res_gen = client.post("/api/v1/questions/generate", json=gen_payload)
    assert res_gen.status_code == 200
    q_data = res_gen.json()
    q_id = q_data["question_id"]
    assert q_id.startswith("price.rel")
    assert "prompt" in q_data

    # 2. Get Next Question for a user
    next_payload = {
        "user_id": "learner-officer-01",
        "competency_id": "price_statistics"
    }
    res_next = client.post("/api/v1/questions/next", json=next_payload)
    assert res_next.status_code == 200
    next_q = res_next.json()
    assert "question_id" in next_q

    # 3. Submit an answer to the generated question
    # We can retrieve internal record to get the exact answer for testing
    from app.statistical_engine.repositories.memory_repositories import question_repo
    internal_rec = question_repo.get_instance(q_id)
    assert internal_rec is not None

    correct_val = internal_rec.correct_option_id if internal_rec.correct_option_id else internal_rec.correct_answer

    sub_payload = {
        "user_id": "learner-officer-01",
        "question_id": q_id,
        "submitted_answer": correct_val,
        "time_taken_seconds": 25
    }
    res_sub = client.post("/api/v1/questions/submit", json=sub_payload)
    assert res_sub.status_code == 200
    sub_data = res_sub.json()
    assert sub_data["correct"] is True
    assert sub_data["score"] == 1.0
    assert sub_data["mastery"]["score"] >= 10.0
    assert "next" in sub_data

    # 4. Check user competencies endpoint
    res_user = client.get("/api/v1/users/learner-officer-01/competencies")
    assert res_user.status_code == 200
    user_state = res_user.json()
    assert "price.price_relative" in user_state
