def test_signup_successfully_adds_new_student(client):
    # Arrange
    activity_name = "Chess Club"
    email = "newstudent@mergington.edu"

    # Act
    response = client.post(f"/activities/{activity_name}/signup", params={"email": email})
    updated = client.get("/activities").json()[activity_name]["participants"]

    # Assert
    assert response.status_code == 200
    assert email in updated
    assert len(updated) == 2


def test_signup_requires_email_param(client):
    # Arrange
    activity_name = "Chess Club"

    # Act
    response = client.post(f"/activities/{activity_name}/signup")

    # Assert
    assert response.status_code == 422


def test_signup_fails_for_missing_activity(client):
    # Arrange
    activity_name = "Unknown Club"
    email = "newstudent@mergington.edu"

    # Act
    response = client.post(f"/activities/{activity_name}/signup", params={"email": email})

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_signup_fails_for_duplicate_student(client):
    # Arrange
    activity_name = "Programming Class"
    email = "emma@mergington.edu"

    # Act
    response = client.post(f"/activities/{activity_name}/signup", params={"email": email})

    # Assert
    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up"


def test_signup_fails_when_activity_is_full(client):
    # Arrange
    activity_name = "Chess Club"
    first_new_email = "second@mergington.edu"
    overflow_email = "third@mergington.edu"

    client.post(f"/activities/{activity_name}/signup", params={"email": first_new_email})

    # Act
    response = client.post(f"/activities/{activity_name}/signup", params={"email": overflow_email})
    current = client.get("/activities").json()[activity_name]["participants"]

    # Assert
    assert response.status_code == 400
    assert response.json()["detail"] == "Activity is full"
    assert overflow_email not in current