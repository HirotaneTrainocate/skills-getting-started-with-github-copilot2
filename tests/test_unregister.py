def test_unregister_successfully_removes_student(client):
    # Arrange
    activity = "Chess Club"
    email = "michael@mergington.edu"
    path = f"/activities/{activity}/unregister"

    # Act
    response = client.delete(path, params={"email": email})
    activities_response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    assert response.json()["message"] == f"Unregistered {email} from {activity}"
    assert email not in activities_response.json()[activity]["participants"]


def test_unregister_fails_for_unknown_activity(client):
    # Arrange
    path = "/activities/Unknown%20Activity/unregister"

    # Act
    response = client.delete(path, params={"email": "student@mergington.edu"})

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_unregister_fails_when_student_not_registered(client):
    # Arrange
    path = "/activities/Chess%20Club/unregister"
    email = "not_registered@mergington.edu"

    # Act
    response = client.delete(path, params={"email": email})

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Student not signed up for this activity"


def test_unregister_fails_when_email_is_missing(client):
    # Arrange
    path = "/activities/Chess%20Club/unregister"

    # Act
    response = client.delete(path)

    # Assert
    assert response.status_code == 422
