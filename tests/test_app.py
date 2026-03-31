from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data
    assert "participants" in data["Chess Club"]

def test_signup():
    # Test successful signup
    response = client.post("/activities/Chess%20Club/signup?email=newstudent@mergington.edu")
    assert response.status_code == 200
    result = response.json()
    assert "Signed up" in result["message"]

    # Verify the participant was added
    response = client.get("/activities")
    data = response.json()
    assert "newstudent@mergington.edu" in data["Chess Club"]["participants"]

def test_signup_nonexistent_activity():
    response = client.post("/activities/Nonexistent/signup?email=test@example.com")
    assert response.status_code == 404
    result = response.json()
    assert "Activity not found" in result["detail"]

def test_unregister():
    # First, sign up a student
    client.post("/activities/Programming%20Class/signup?email=temp@mergington.edu")

    # Now unregister
    response = client.post("/activities/Programming%20Class/unregister?email=temp@mergington.edu")
    assert response.status_code == 200
    result = response.json()
    assert "Unregistered" in result["message"]

    # Verify the participant was removed
    response = client.get("/activities")
    data = response.json()
    assert "temp@mergington.edu" not in data["Programming Class"]["participants"]

def test_unregister_not_signed_up():
    response = client.post("/activities/Gym%20Class/unregister?email=notsignedup@mergington.edu")
    assert response.status_code == 400
    result = response.json()
    assert "Not signed up" in result["detail"]

def test_unregister_nonexistent_activity():
    response = client.post("/activities/Nonexistent/unregister?email=test@example.com")
    assert response.status_code == 404
    result = response.json()
    assert "Activity not found" in result["detail"]