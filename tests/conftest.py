import pytest
import copy
from fastapi.testclient import TestClient
from src.app import app, activities


@pytest.fixture
def client():
    """Provide a test client for the FastAPI app"""
    return TestClient(app)


@pytest.fixture(autouse=True)
def reset_activities():
    """Reset activities to initial state before each test"""
    # Store initial state
    initial_activities = {
        "Chess Club": {
            "description": "Learn strategies and compete in chess tournaments",
            "schedule": "Fridays, 3:30 PM - 5:00 PM",
            "max_participants": 12,
            "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
        },
        "Programming Class": {
            "description": "Learn programming fundamentals and build software projects",
            "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
            "max_participants": 20,
            "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
        },
        "Gym Class": {
            "description": "Physical education and sports activities",
            "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
            "max_participants": 30,
            "participants": ["john@mergington.edu", "olivia@mergington.edu"]
        },
        "Basketball Team": {
            "description": "Practice teamwork and compete in interschool basketball games",
            "schedule": "Mondays and Thursdays, 4:00 PM - 5:30 PM",
            "max_participants": 15,
            "participants": ["alex@mergington.edu", "nina@mergington.edu"]
        },
        "Swimming Club": {
            "description": "Improve swimming skills and prepare for swim meets",
            "schedule": "Tuesdays and Saturdays, 4:00 PM - 5:30 PM",
            "max_participants": 18,
            "participants": ["sara@mergington.edu", "leo@mergington.edu"]
        },
        "Art Club": {
            "description": "Explore painting, drawing, and mixed media art projects",
            "schedule": "Wednesdays, 3:30 PM - 5:00 PM",
            "max_participants": 20,
            "participants": ["maya@mergington.edu", "julia@mergington.edu"]
        },
        "Drama Club": {
            "description": "Practice acting, stagecraft, and put on school plays",
            "schedule": "Fridays, 4:00 PM - 6:00 PM",
            "max_participants": 25,
            "participants": ["carter@mergington.edu", "lena@mergington.edu"]
        },
        "Debate Team": {
            "description": "Prepare for debate tournaments and strengthen public speaking skills",
            "schedule": "Tuesdays and Thursdays, 5:00 PM - 6:30 PM",
            "max_participants": 16,
            "participants": ["james@mergington.edu", "sophia@mergington.edu"]
        },
        "Math Olympiad": {
            "description": "Solve challenging math problems and compete in academic contests",
            "schedule": "Wednesdays and Fridays, 3:30 PM - 5:00 PM",
            "max_participants": 18,
            "participants": ["noah@mergington.edu", "mia@mergington.edu"]
        }
    }
    
    # Clear and restore activities
    activities.clear()
    activities.update(copy.deepcopy(initial_activities))
    
    yield
    
    # Cleanup after test
    activities.clear()
    activities.update(copy.deepcopy(initial_activities))
