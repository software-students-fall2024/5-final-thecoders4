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
    response = client.get('/')
    assert response.status_code == 200
    assert b"Find Your Perfect Dog Companion" in response.data
    assert b"Answer a few quick questions to discover the dog breed that suits your likestyle best." in response.data

def test_404(client):  # pylint: disable=redefined-outer-name
    """Test a non-existent route, expecting 404 error"""
    response = client.get("/non-existent-route")
    assert response.status_code == 404

def test_question1(client):  # pylint: disable=redefined-outer-name
    response = client.get('/question1')
    assert response.status_code == 200
    assert b"Find Your Perfect Dog Companion" in response.data
    assert b"Choose Your Preference On Following Questions" in response.data
    questions= [b"Affectionate with Family:", b"Good With Young Children:", b"Good With Other Dogs:"]
    for question in questions:
        assert question in response.data

def test_question2(client):  # pylint: disable=redefined-outer-name
    response = client.get('/question2')
    assert response.status_code == 200
    assert b"Find Your Perfect Dog Companion" in response.data
    assert b"Choose Your Preference On Following Questions" in response.data
    questions= [b"Shedding Level:", b"Coat Grooming Frequency:", b"Drooling Level:"]
    for question in questions:
        assert question in response.data

def test_question3(client):  # pylint: disable=redefined-outer-name
    response = client.get('/question3')
    assert response.status_code == 200
    assert b"Find Your Perfect Dog Companion" in response.data
    assert b"Choose Your Preference On Following Questions" in response.data
    questions= [b"Openness to Strangers:", b"Playfulness Level:", b"Watchdog/Protective Nature:", b"Adaptability Level:"]
    for question in questions:
        assert question in response.data

def test_question4(client):  # pylint: disable=redefined-outer-name
    response = client.get('/question4')
    assert response.status_code == 200
    assert b"Find Your Perfect Dog Companion" in response.data
    assert b"Choose Your Preference On Following Questions" in response.data
    questions= [b"Trainability Level:", b"Energy Level:", b"Barking Level:", b"Mental Stimulation Needs:"]
    for question in questions:
        assert question in response.data