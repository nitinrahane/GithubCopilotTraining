def test_signup_unregister_signup_flow(client):
    # Arrange
    activity_name = "Science Club"
    email = "flow@mergington.edu"

    # Act
    signup_response = client.post(f"/activities/{activity_name}/signup", params={"email": email})
    unregister_response = client.post(f"/activities/{activity_name}/unregister", params={"email": email})
    resubscribe_response = client.post(f"/activities/{activity_name}/signup", params={"email": email})
    participants = client.get("/activities").json()[activity_name]["participants"]

    # Assert
    assert signup_response.status_code == 200
    assert unregister_response.status_code == 200
    assert resubscribe_response.status_code == 200
    assert email in participants


def test_capacity_then_unregister_allows_new_signup(client):
    # Arrange
    activity_name = "Chess Club"
    second_student = "second@mergington.edu"
    overflow_student = "overflow@mergington.edu"

    # Act
    fill_response = client.post(f"/activities/{activity_name}/signup", params={"email": second_student})
    overflow_response = client.post(
        f"/activities/{activity_name}/signup", params={"email": overflow_student}
    )
    free_spot_response = client.post(
        f"/activities/{activity_name}/unregister", params={"email": second_student}
    )
    retry_response = client.post(
        f"/activities/{activity_name}/signup", params={"email": overflow_student}
    )
    participants = client.get("/activities").json()[activity_name]["participants"]

    # Assert
    assert fill_response.status_code == 200
    assert overflow_response.status_code == 400
    assert free_spot_response.status_code == 200
    assert retry_response.status_code == 200
    assert overflow_student in participants


def test_multiple_students_add_and_remove_flow(client):
    # Arrange
    activity_name = "Science Club"
    first_email = "first@mergington.edu"
    second_email = "second@mergington.edu"
    third_email = "third@mergington.edu"

    # Act
    first = client.post(f"/activities/{activity_name}/signup", params={"email": first_email})
    second = client.post(f"/activities/{activity_name}/signup", params={"email": second_email})
    third = client.post(f"/activities/{activity_name}/signup", params={"email": third_email})
    remove = client.post(f"/activities/{activity_name}/unregister", params={"email": second_email})
    participants = client.get("/activities").json()[activity_name]["participants"]

    # Assert
    assert first.status_code == 200
    assert second.status_code == 200
    assert third.status_code == 200
    assert remove.status_code == 200
    assert first_email in participants
    assert second_email not in participants
    assert third_email in participants
    assert len(participants) == 3