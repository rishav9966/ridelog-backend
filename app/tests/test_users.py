def test_create_user_success(client):
    res = client.post(
        "/users/",
        json={"email": "user1@example.com", "name": "user1", "password": "user@123"},
    )
    res_json = res.json()
    assert res.status_code == 200
    assert all(item in res_json for item in ["id", "email", "name"])
    assert not(all(item in res_json for item in ["hashed_password", "password"]))

def test_create_user_weak_password(client):
    res = client.post(
        "/users/",
        json={"email": "user1@example.com", "name": "user1", "password": "user"},
    )
    assert res.status_code == 422


def test_create_user_duplicate_email(client, test_user):
    res = client.post(
        "/users/",
        json={
            "email": test_user.email,
            "name": test_user.name,
            "password": "Str0ng!Pass123",
        },
    )
    res_json = res.json()
    assert res.status_code == 400
    assert res_json["detail"] == "Email already registered"
