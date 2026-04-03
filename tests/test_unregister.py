def test_unregister_successfully_removes_student(client):
    # Arrange
    activity_name = "Programming Class"
    email = "emma@mergington.edu"

    # Act
    response = client.post(f"/activities/{activity_name}/unregister", params={"email": email})
    updated = client.get("/activities").json()[activity_name]["participants"]

    # Assert
    assert response.status_code == 200
    assert email not in updated
    assert len(updated) == 1


def test_unregister_requires_email_param(client):
    # Arrange
    activity_name = "Programming Class"

    # Act
    response = client.post(f"/activities/{activity_name}/unregister")

    # Assert
    assert response.status_code == 422


def test_unregister_fails_for_missing_activity(client):
    # Arrange
    activity_name = "Unknown Club"
    email = "student@mergington.edu"

    # Act
    response = client.post(f"/activities/{activity_name}/unregister", params={"email": email})

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_unregister_fails_when_student_not_signed_up(client):
    # Arrange
    activity_name = "Science Club"
    email = "notthere@mergington.edu"

    # Act
    response = client.post(f"/activities/{activity_name}/unregister", params={"email": email})

    # Assert
    assert response.status_code == 400
    assert response.json()["detail"] == "Student not signed up for this activity"


def test_student_can_signup_again_after_unregister(client):
    # Arrange
    activity_name = "Programming Class"
    email = "emma@mergington.edu"

    client.post(f"/activities/{activity_name}/unregister", params={"email": email})

    # Act
    response = client.post(f"/activities/{activity_name}/signup", params={"email": email})
    updated = client.get("/activities").json()[activity_name]["participants"]

    # Assert
    assert response.status_code == 200
    assert email in updated