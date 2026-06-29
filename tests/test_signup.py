def test_signup_successfully_adds_student(client):
    # Arrange
    activity = "Chess Club"
    email = "new_student@mergington.edu"
    path = f"/activities/{activity}/signup"

    # Act
    response = client.post(path, params={"email": email})
    activities_response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    assert response.json()["message"] == f"Signed up {email} for {activity}"
    assert email in activities_response.json()[activity]["participants"]


def test_signup_fails_for_unknown_activity(client):
    # Arrange
    path = "/activities/Unknown%20Activity/signup"

    # Act
    response = client.post(path, params={"email": "student@mergington.edu"})

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_signup_fails_when_student_already_registered(client):
    # Arrange
    activity = "Chess Club"
    existing_email = "michael@mergington.edu"
    path = f"/activities/{activity}/signup"

    # Act
    response = client.post(path, params={"email": existing_email})

    # Assert
    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up for this activity"


def test_signup_fails_when_email_is_missing(client):
    # Arrange
    path = "/activities/Chess%20Club/signup"

    # Act
    response = client.post(path)

    # Assert
    assert response.status_code == 422


def test_signup_supports_url_encoded_activity_name(client):
    # Arrange
    activity_path = "/activities/Chess%20Club/signup"
    email = "encoded_name_test@mergington.edu"

    # Act
    response = client.post(activity_path, params={"email": email})

    # Assert
    assert response.status_code == 200
    assert response.json()["message"] == f"Signed up {email} for Chess Club"
