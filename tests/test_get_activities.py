def test_get_activities_returns_expected_structure(client):
    # Arrange
    expected_fields = {"description", "schedule", "max_participants", "participants"}

    # Act
    response = client.get("/activities")
    payload = response.json()

    # Assert
    assert response.status_code == 200
    assert isinstance(payload, dict)
    assert len(payload) == 3

    for activity_data in payload.values():
        assert expected_fields.issubset(activity_data.keys())
        assert isinstance(activity_data["participants"], list)


def test_root_redirects_to_static_index(client):
    # Arrange
    target_location = "/static/index.html"

    # Act
    response = client.get("/", follow_redirects=False)

    # Assert
    assert response.status_code in (302, 307)
    assert response.headers["location"] == target_location