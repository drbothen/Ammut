import pytest
from fastapi.testclient import TestClient

from src.server.main import app
from src.server.models.schemas import TargetProfile, TargetType, TechnologyStack

client = TestClient(app)

@pytest.fixture
def sample_target_profile() -> TargetProfile:
    """Provides a sample TargetProfile for testing."""
    return TargetProfile(
        target="http://testserver.com",
        target_type=TargetType.WEB_APPLICATION,
        technologies=[TechnologyStack.PYTHON, TechnologyStack.NGINX],
        ip_addresses=["192.168.1.1"],
        attack_surface_score=7.5,
        risk_level="high",
        confidence_score=0.9
    )

def test_analyze_target():
    """Test the /analyze endpoint."""
    response = client.post("/api/intelligent-decision/analyze", json={"target": "http://example.com"})
    assert response.status_code == 200
    profile = response.json()
    assert profile["target"] == "http://example.com"
    assert profile["target_type"] == "web_application"
    assert profile["risk_level"] is not None

def test_select_tools(sample_target_profile: TargetProfile):
    """Test the /select-tools endpoint."""
    response = client.post(
        "/api/intelligent-decision/select-tools",
        json={"profile": sample_target_profile.model_dump(), "objective": "comprehensive"}
    )
    assert response.status_code == 200
    tools = response.json()
    assert isinstance(tools, list)
    assert len(tools) > 0
    assert "nuclei" in tools

def test_optimize_parameters(sample_target_profile: TargetProfile):
    """Test the /optimize-parameters endpoint."""
    response = client.post(
        "/api/intelligent-decision/optimize-parameters",
        json={"tool_name": "nuclei", "profile": sample_target_profile.model_dump()}
    )
    assert response.status_code == 200
    params = response.json()
    assert isinstance(params, dict)
    assert params["severity"] == "critical,high"

def test_generate_chain(sample_target_profile: TargetProfile):
    """Test the /generate-chain endpoint."""
    response = client.post(
        "/api/intelligent-decision/generate-chain",
        json={"profile": sample_target_profile.model_dump(), "objective": "comprehensive"}
    )
    assert response.status_code == 200
    chain = response.json()
    assert "steps" in chain
    assert len(chain["steps"]) > 0
    assert chain["steps"][0]["tool"] is not None
