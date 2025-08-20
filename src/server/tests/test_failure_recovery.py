import pytest
from fastapi.testclient import TestClient
from typing import Dict, Any, List

from src.server.main import app
from src.server.models.schemas import FailureAnalysisRequest, FailureAnalysisResponse

client = TestClient(app)

@pytest.mark.parametrize(
    "request_payload, expected_response",
    [
        (
            FailureAnalysisRequest(
                error_output="Error: Connection timed out after 30 seconds",
                exit_code=124
            ),
            {
                "failure_type": "timeout",
                "confidence": 0.8,  # 0.3 for pattern + 0.5 for exit code
                "recovery_strategies": [
                    "Increase timeout values",
                    "Reduce thread count",
                    "Use alternative faster tool",
                    "Split target into smaller chunks"
                ],
                "alternative_tools": []
            }
        ),
        (
            FailureAnalysisRequest(
                error_output="bash: nmap: command not found",
                exit_code=127
            ),
            {
                "failure_type": "not_found",
                "confidence": 0.4, # 0.3 for pattern + 0.1 for exit code
                "recovery_strategies": [],
                "alternative_tools": ["rustscan", "masscan", "zmap"]
            }
        ),
        (
            FailureAnalysisRequest(
                error_output="(hydra) attacking ftp://127.0.0.1:21/",
                exit_code=0
            ),
            {
                "failure_type": "unknown",
                "confidence": 0.0,
                "recovery_strategies": [],
                "alternative_tools": ["medusa", "ncrack", "patator"]
            }
        ),
    ]
)
def test_analyze_failure(
    request_payload: FailureAnalysisRequest,
    expected_response: Dict[str, Any]
):
    response = client.post("/api/failure-recovery/analyze-failure", json=request_payload.dict())
    assert response.status_code == 200
    
    result = FailureAnalysisResponse(**response.json())
    
    assert result.failure_type == expected_response["failure_type"]
    assert result.confidence == pytest.approx(expected_response["confidence"], abs=1e-2)
    assert sorted(result.recovery_strategies) == sorted(expected_response["recovery_strategies"])
    assert sorted(result.alternative_tools) == sorted(expected_response["alternative_tools"])
