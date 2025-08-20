import pytest
from fastapi.testclient import TestClient

from src.server.main import app

client = TestClient(app)


def test_get_tool_command():
    response = client.post(
        "/api/tool-manager/command",
        json={"tool": "nmap", "target": "localhost"},
    )
    assert response.status_code == 200
    assert "nmap -sV -sC -T4 localhost" in response.text


def test_get_category_tools():
    response = client.get("/api/tool-manager/tools/web_recon")
    assert response.status_code == 200
    tools = response.json()
    assert "nmap" in tools
    assert "gobuster" in tools


def test_suggest_tools_for_web_challenge():
    response = client.post(
        "/api/tool-manager/suggest-tools",
        json={"description": "This is a web challenge with sql injection", "category": "web"},
    )
    assert response.status_code == 200
    suggestions = response.json()
    assert "sqlmap" in suggestions


def test_suggest_tools_for_crypto_challenge():
    response = client.post(
        "/api/tool-manager/suggest-tools",
        json={"description": "This challenge involves rsa encryption", "category": "crypto"},
    )
    assert response.status_code == 200
    suggestions = response.json()
    assert "rsatool" in suggestions


def test_invalid_category():
    response = client.get("/api/tool-manager/tools/invalid_category")
    assert response.status_code == 200
    assert response.json() == []
