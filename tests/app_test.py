"""
This module contains unit tests for ml-client.
"""

import io
import pytest
from pathlib import Path

from app import create_app

@pytest.fixture
def client():
    """Fixture for the Flask test client."""
    app = create_app(skip_initialization=True)
    app.config["TESTING"] = True
    with app.test_client() as client:  
        yield client

def test_root1(client):  # pylint: disable=redefined-outer-name
    response = client.get("/")
    #html_text = response.data#.decode("utf-8")
    #assert "Start Recording" in html_text
    assert response.status_code == 200

def test_404(client):  # pylint: disable=redefined-outer-name
    """Test a non-existent route, expecting 404 error"""
    response = client.get("/non-existent-route")
    assert response.status_code == 404