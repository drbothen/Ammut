import pytest
from fastapi.testclient import TestClient
from typing import List, Dict, Any
from datetime import datetime

from src.server.main import app
from src.server.models.enums import ErrorType
from src.server.models.schemas import RecoveryAction

client = TestClient(app)

@pytest.mark.parametrize(
    "context_payload, expected_actions",
    [
        (
            {
                "tool_name": "nmap",
                "target": "127.0.0.1",
                "parameters": {"-p-": ""},
                "error_type": ErrorType.UNKNOWN,
                "error_message": "Timeout while connecting to host",
                "attempt_count": 1,
                "timestamp": datetime.now().isoformat(),
                "stack_trace": "",
                "system_resources": {},
            },
            [RecoveryAction.RETRY_WITH_BACKOFF, RecoveryAction.RETRY_WITH_REDUCED_SCOPE, RecoveryAction.SWITCH_TO_ALTERNATIVE_TOOL],
        ),
        (
            {
                "tool_name": "gobuster",
                "target": "https://example.com",
                "parameters": {"wordlist": "/usr/share/wordlists/dirb/common.txt"},
                "error_type": ErrorType.UNKNOWN,
                "error_message": "command not found",
                "attempt_count": 1,
                "timestamp": datetime.now().isoformat(),
                "stack_trace": "",
                "system_resources": {},
            },
            [RecoveryAction.SWITCH_TO_ALTERNATIVE_TOOL, RecoveryAction.ESCALATE_TO_HUMAN],
        ),
        (
            {
                "tool_name": "unknown_tool",
                "target": "some_target",
                "parameters": {},
                "error_type": ErrorType.UNKNOWN,
                "error_message": "an unknown error occurred",
                "attempt_count": 1,
                "timestamp": datetime.now().isoformat(),
                "stack_trace": "",
                "system_resources": {},
            },
            [RecoveryAction.ESCALATE_TO_HUMAN],
        ),
        (
            {
                "tool_name": "nmap",
                "target": "127.0.0.1",
                "parameters": {},
                "error_type": ErrorType.UNKNOWN,
                "error_message": "Error: Connection timed out after 30 seconds",
                "attempt_count": 1,
                "timestamp": datetime.now().isoformat(),
                "stack_trace": "",
                "system_resources": {},
                "exit_code": 124,
            },
            [RecoveryAction.ADJUST_PARAMETERS],
        ),
    ],
)
def test_get_recovery_strategies(context_payload: Dict[str, Any], expected_actions: List[RecoveryAction]):
    response = client.post("/api/error-recovery/get-recovery-strategies", json=context_payload)
    assert response.status_code == 200
    
    strategies = response.json()
    assert isinstance(strategies, list)
    
    actions = [strategy['action'] for strategy in strategies]
    assert sorted(actions) == sorted([action.value for action in expected_actions])

    # Check for specific parameters in known strategies
    if context_payload["tool_name"] == "nmap":
        for strategy in strategies:
            if strategy['action'] == RecoveryAction.SWITCH_TO_ALTERNATIVE_TOOL:
                assert 'alternative_tools' in strategy['parameters']
                assert 'rustscan' in strategy['parameters']['alternative_tools']
