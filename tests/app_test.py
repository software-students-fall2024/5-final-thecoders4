"""
This module contains unit tests for the web app.
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
        
def test_question1_post(client):
    # Simulate POST request with form data
    response = client.post(
        '/question1',
        data={
            "family": "lovey-dovey",
            "children": "good",
            "dog": "good"
        },
        follow_redirects=True
    )

    # Assert the session values are correctly set
    with client.session_transaction() as sess:
        assert sess["affectionate_with_family"] == "lovey-dovey"
        assert sess["good_with_young_children"] == "good"
        assert sess["good_with_other_dogs"] == "good"

    # Assert the redirect to /question2
    assert response.status_code == 200
    assert b"Find Your Perfect Dog Companion with Physical Traits" in response.data 
    
def test_question2_post(client):
    # Simulate POST request with form data
    response = client.post(
        '/question2',
        data={
            "shedding": "low",
            "coat": "minimal",
            "drooling": "none"
        },
        follow_redirects=True
    )

    # Assert the session values are correctly set
    with client.session_transaction() as sess:
        assert sess["shedding_level"] == "low"
        assert sess["coat_grooming_frequency"] == "minimal"
        assert sess["drooling_level"] == "none"

    # Assert the redirect to /question3
    assert response.status_code == 200
    assert b"Find Your Perfect Dog Companion with Social Traits" in response.data

def test_question3_post(client):
    # Simulate POST request with form data
    response = client.post(
        '/question3',
        data={
            "openness": "friendly",
            "playfulness": "high",
            "nature": "protective",
            "adaptability": "adaptable"
        },
        follow_redirects=True
    )

    # Assert the session values are correctly set
    with client.session_transaction() as sess:
        assert sess["openness_to_strangers"] == "friendly"
        assert sess["playfulness_level"] == "high"
        assert sess["watchgod/protective_nature"] == "protective"
        assert sess["adaptability_level"] == "adaptable"

    # Assert the redirect to /question4
    assert response.status_code == 200
    assert b"Find Your Perfect Dog Companion with Personalities" in response.data

def test_question4_post(client):
    # Simulate a POST request to /question4 with form data
    response = client.post(
        '/question4',
        data={
            "trainability": "high",
            "energy": "medium",
            "barking": "low",
            "mental": "moderate"
        },
        follow_redirects=False  # No need to follow redirects for this test
    )

    # Assert that the session values are correctly set
    with client.session_transaction() as sess:
        assert sess["trainability_level"] == "high"
        assert sess["energy_level"] == "medium"
        assert sess["barking_level"] == "low"
        assert sess["mental_stimulation_needs"] == "moderate"

    # Assert that the response is a redirect to /result
    assert response.status_code == 302  # Redirect status code
    assert response.location.endswith('/result')  # Redirect URL

def test_result(client):
    # Mock session data to simulate user input
    with client.session_transaction() as sess:
        sess["affectionate_with_family"] = "lovey-dovey"
        sess["good_with_young_children"] = "good"
        sess["good_with_other_dogs"] = "good"
        sess["shedding_level"] = "everywhere"
        sess["coat_grooming_frequency"] = "daily"
        sess["drooling_level"] = "always"
        sess["openness_to_strangers"] = "everyone"
        sess["playfulness_level"] = "non_stop"
        sess["watchgod/protective_nature"] = "vigilant"
        sess["adaptability_level"] = "adaptable"
        sess["trainability_level"] = "eager"
        sess["energy_level"] = "high"
        sess["barking_level"] = "vocal"
        sess["mental_stimulation_needs"] = "job"

        # Mock database results
        sess["mock_docs"] = [
            {"Breed": "Golden Retriever", "Affectionate With Family": 5, "Good With Young Children": 5},
            {"Breed": "Labrador Retriever", "Affectionate With Family": 4, "Good With Young Children": 4},
        ]

    # Call the result route
    response = client.get('/result')

    # Assertions
    assert response.status_code == 200
    assert b"Golden Retriever" in response.data
    assert b"Labrador Retriever" in response.data

def test_result_low_values(client):
    # Mock session data to simulate user input
    with client.session_transaction() as sess:
        sess["affectionate_with_family"] = "independent"
        sess["good_with_young_children"] = "not_recommended"
        sess["good_with_other_dogs"] = "not_recommended"
        sess["shedding_level"] = "no_shedding"
        sess["coat_grooming_frequency"] = "monthly"
        sess["drooling_level"] = "less"
        sess["openness_to_strangers"] = "reserved"
        sess["playfulness_level"] = "only"
        sess["watchgod/protective_nature"] = "mine"
        sess["adaptability_level"] = "routine"
        sess["trainability_level"] = "self-willed"
        sess["energy_level"] = "couch_potato"
        sess["barking_level"] = "alert"
        sess["mental_stimulation_needs"] = "lounge"

        # Mock database results for this specific scenario
        sess["mock_docs"] = [
            {"Breed": "Chihuahua", "Affectionate With Family": 2, "Good With Young Children": 1},
            {"Breed": "Pekingese", "Affectionate With Family": 1, "Good With Young Children": 2},
        ]

    # Call the result route
    response = client.get('/result')

    # Assertions
    assert response.status_code == 200
    assert b"Chihuahua" in response.data
    assert b"Pekingese" in response.data

