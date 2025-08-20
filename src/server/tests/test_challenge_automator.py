import pytest
from fastapi.testclient import TestClient

from src.server.main import app

client = TestClient(app)


def test_solve_web_challenge():
    """Test solving a web challenge."""
    challenge_data = {
        "name": "Web Challenge 1",
        "category": "web",
        "description": "A simple web challenge.",
        "target": "http://example.com"
    }
    response = client.post("/api/challenge-automator/solve", json=challenge_data)
    assert response.status_code == 200
    solution = response.json()
    assert solution["challenge_id"] == "Web Challenge 1"
    assert solution["status"] in ["solved", "needs_manual_intervention"]
    assert len(solution["automated_steps"]) > 0
    assert "nmap" in solution["automated_steps"][0]["tools_used"]


def test_solve_crypto_challenge():
    """Test solving a crypto challenge."""
    challenge_data = {
        "name": "Crypto Challenge 1",
        "category": "crypto",
        "description": "A simple crypto challenge.",
        "target": "ciphertext.txt"
    }
    response = client.post("/api/challenge-automator/solve", json=challenge_data)
    assert response.status_code == 200
    solution = response.json()
    assert solution["challenge_id"] == "Crypto Challenge 1"
    assert solution["status"] in ["solved", "needs_manual_intervention"]
    assert len(solution["automated_steps"]) > 0
    assert "ciphey" in solution["automated_steps"][0]["tools_used"]
