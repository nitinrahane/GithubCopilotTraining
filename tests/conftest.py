import copy

import pytest
from fastapi.testclient import TestClient

from src.app import activities, app


@pytest.fixture
def test_activities():
    return {
        "Chess Club": {
            "description": "Learn strategies and compete in chess tournaments",
            "schedule": "Fridays, 3:30 PM - 5:00 PM",
            "max_participants": 2,
            "participants": ["michael@mergington.edu"],
        },
        "Programming Class": {
            "description": "Learn programming fundamentals and build software projects",
            "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
            "max_participants": 3,
            "participants": ["emma@mergington.edu", "sophia@mergington.edu"],
        },
        "Science Club": {
            "description": "STEM experiments and scientific inquiry projects",
            "schedule": "Tuesdays, 3:30 PM - 4:30 PM",
            "max_participants": 4,
            "participants": ["mia@mergington.edu"],
        },
    }


@pytest.fixture(autouse=True)
def reset_activities(test_activities):
    activities.clear()
    activities.update(copy.deepcopy(test_activities))
    yield
    activities.clear()


@pytest.fixture
def client():
    return TestClient(app)