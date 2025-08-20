import pytest
from fastapi.testclient import TestClient

from src.server.main import app

client = TestClient(app)


def test_create_banner():
    """Test the /banner endpoint."""
    response = client.post("/api/visual-engine/banner")
    assert response.status_code == 200
    assert "HexStrike AI" in response.text


def test_create_progress_bar():
    """Test the /progress-bar endpoint."""
    request_data = {"current": 50, "total": 100, "width": 50, "tool": "test"}
    response = client.post("/api/visual-engine/progress-bar", json=request_data)
    assert response.status_code == 200
    assert "50.0%" in response.text
    assert "test" in response.text

def test_render_progress_bar():
    """Test the /render-progress-bar endpoint."""
    request_data = {"progress": 0.75, "label": "Testing"}
    response = client.post("/api/visual-engine/render-progress-bar", json=request_data)
    assert response.status_code == 200
    assert "75.0%" in response.text
    assert "Testing" in response.text

def test_create_live_dashboard():
    """Test the /live-dashboard endpoint."""
    request_data = {"processes": {123: {"status": "running", "command": "nmap -sV"}}}
    response = client.post("/api/visual-engine/live-dashboard", json=request_data)
    assert response.status_code == 200
    assert "HEXSTRIKE LIVE DASHBOARD" in response.text
    assert "PID 123" in response.text

def test_format_vulnerability_card():
    """Test the /vulnerability-card endpoint."""
    request_data = {"vuln_data": {"severity": "CRITICAL", "name": "SQL Injection"}}
    response = client.post("/api/visual-engine/vulnerability-card", json=request_data)
    assert response.status_code == 200
    assert "VULNERABILITY DETECTED" in response.text
    assert "SQL Injection" in response.text

def test_format_error_card():
    """Test the /error-card endpoint."""
    request_data = {"error_type": "TIMEOUT", "tool_name": "Nmap", "error_message": "Host not responding"}
    response = client.post("/api/visual-engine/error-card", json=request_data)
    assert response.status_code == 200
    assert "ERROR DETECTED" in response.text
    assert "Nmap" in response.text

def test_format_tool_status():
    """Test the /tool-status endpoint."""
    request_data = {"tool_name": "Nuclei", "status": "RUNNING", "target": "example.com"}
    response = client.post("/api/visual-engine/tool-status", json=request_data)
    assert response.status_code == 200
    assert "NUCLEI" in response.text
    assert "RUNNING" in response.text

def test_format_highlighted_text():
    """Test the /highlighted-text endpoint."""
    request_data = {"text": "Important", "highlight_type": "YELLOW"}
    response = client.post("/api/visual-engine/highlighted-text", json=request_data)
    assert response.status_code == 200
    assert "Important" in response.text

def test_format_vulnerability_severity():
    """Test the /vulnerability-severity endpoint."""
    request_data = {"severity": "HIGH", "count": 5}
    response = client.post("/api/visual-engine/vulnerability-severity", json=request_data)
    assert response.status_code == 200
    assert "HIGH" in response.text
    assert "(5)" in response.text

def test_create_section_header():
    """Test the /section-header endpoint."""
    request_data = {"title": "Reconnaissance"}
    response = client.post("/api/visual-engine/section-header", json=request_data)
    assert response.status_code == 200
    assert "RECONNAISSANCE" in response.text

def test_format_command_execution():
    """Test the /command-execution endpoint."""
    request_data = {"command": "whoami", "status": "SUCCESS"}
    response = client.post("/api/visual-engine/command-execution", json=request_data)
    assert response.status_code == 200
    assert "whoami" in response.text
    assert "SUCCESS" in response.text
