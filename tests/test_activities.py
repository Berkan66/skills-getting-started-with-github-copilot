import pytest


class TestGetActivities:
    """Test GET /activities endpoint"""
    
    def test_get_activities_returns_all_activities(self, client):
        # Arrange - test data already loaded in fixture
        
        # Act
        response = client.get("/activities")
        
        # Assert
        assert response.status_code == 200
        activities = response.json()
        assert len(activities) == 9
        assert "Chess Club" in activities
        assert "Programming Class" in activities
    
    def test_get_activities_returns_correct_structure(self, client):
        # Arrange
        
        # Act
        response = client.get("/activities")
        activities = response.json()
        
        # Assert
        activity = activities["Chess Club"]
        assert "description" in activity
        assert "schedule" in activity
        assert "max_participants" in activity
        assert "participants" in activity
        assert isinstance(activity["participants"], list)


class TestSignupForActivity:
    """Test POST /activities/{activity_name}/signup endpoint"""
    
    def test_signup_success(self, client):
        # Arrange
        activity_name = "Chess Club"
        email = "newstudent@mergington.edu"
        
        # Act
        response = client.post(
            f"/activities/{activity_name}/signup?email={email}"
        )
        
        # Assert
        assert response.status_code == 200
        result = response.json()
        assert "Signed up" in result["message"]
        assert email in result["message"]
    
    def test_signup_adds_participant_to_activity(self, client):
        # Arrange
        activity_name = "Chess Club"
        email = "newstudent@mergington.edu"
        
        # Act
        response = client.post(
            f"/activities/{activity_name}/signup?email={email}"
        )
        activities_response = client.get("/activities")
        activities = activities_response.json()
        
        # Assert
        assert response.status_code == 200
        assert email in activities[activity_name]["participants"]
    
    def test_signup_duplicate_email_returns_400(self, client):
        # Arrange
        activity_name = "Chess Club"
        email = "michael@mergington.edu"  # Already signed up
        
        # Act
        response = client.post(
            f"/activities/{activity_name}/signup?email={email}"
        )
        
        # Assert
        assert response.status_code == 400
        assert "already signed up" in response.json()["detail"]
    
    def test_signup_nonexistent_activity_returns_404(self, client):
        # Arrange
        activity_name = "Nonexistent Club"
        email = "student@mergington.edu"
        
        # Act
        response = client.post(
            f"/activities/{activity_name}/signup?email={email}"
        )
        
        # Assert
        assert response.status_code == 404
        assert "not found" in response.json()["detail"]
    
    def test_signup_increases_participant_count(self, client):
        # Arrange
        activity_name = "Programming Class"
        email = "newstudent@mergington.edu"
        activities_before = client.get("/activities").json()
        initial_count = len(activities_before[activity_name]["participants"])
        
        # Act
        client.post(f"/activities/{activity_name}/signup?email={email}")
        activities_after = client.get("/activities").json()
        
        # Assert
        new_count = len(activities_after[activity_name]["participants"])
        assert new_count == initial_count + 1


class TestUnregisterFromActivity:
    """Test POST /activities/{activity_name}/unregister endpoint"""
    
    def test_unregister_success(self, client):
        # Arrange
        activity_name = "Chess Club"
        email = "michael@mergington.edu"  # Already signed up
        
        # Act
        response = client.post(
            f"/activities/{activity_name}/unregister?email={email}"
        )
        
        # Assert
        assert response.status_code == 200
        result = response.json()
        assert "Unregistered" in result["message"]
    
    def test_unregister_removes_participant(self, client):
        # Arrange
        activity_name = "Chess Club"
        email = "michael@mergington.edu"
        
        # Act
        client.post(f"/activities/{activity_name}/unregister?email={email}")
        activities_response = client.get("/activities")
        activities = activities_response.json()
        
        # Assert
        assert email not in activities[activity_name]["participants"]
    
    def test_unregister_decreases_participant_count(self, client):
        # Arrange
        activity_name = "Programming Class"
        email = "emma@mergington.edu"
        activities_before = client.get("/activities").json()
        initial_count = len(activities_before[activity_name]["participants"])
        
        # Act
        client.post(f"/activities/{activity_name}/unregister?email={email}")
        activities_after = client.get("/activities").json()
        
        # Assert
        new_count = len(activities_after[activity_name]["participants"])
        assert new_count == initial_count - 1
    
    def test_unregister_nonexistent_participant_returns_400(self, client):
        # Arrange
        activity_name = "Chess Club"
        email = "notregistered@mergington.edu"
        
        # Act
        response = client.post(
            f"/activities/{activity_name}/unregister?email={email}"
        )
        
        # Assert
        assert response.status_code == 400
        assert "not registered" in response.json()["detail"]
    
    def test_unregister_nonexistent_activity_returns_404(self, client):
        # Arrange
        activity_name = "Nonexistent Club"
        email = "student@mergington.edu"
        
        # Act
        response = client.post(
            f"/activities/{activity_name}/unregister?email={email}"
        )
        
        # Assert
        assert response.status_code == 404
        assert "not found" in response.json()["detail"]
