def test_login_success(client, test_user):
    res = client.post(
        "/users/login",
        json={"email": test_user.email, "password": "Str0ng!Pass123"},
    )
    assert res.status_code == 200
    res_json = res.json()
    assert "access_token" in res_json
    assert res_json["access_token"]


def test_login_wrong_password(client, test_user):
    res = client.post(
        "/users/login",
        json={"email": test_user.email, "password": "Str0ng!Pass1234"},
    )
    assert res.status_code == 401


def test_login_unknown_email(client):
    res = client.post(
        "/users/login",
        json={"email": "hello@mail.com", "password": "test"},
    )
    assert res.status_code == 401


def test_me_unauthorized(client):
    res = client.get("/users/me")
    assert res.status_code == 401


def test_me_authorized(client, auth_headers):
    res = client.get("/users/me", headers=auth_headers)
    assert res.status_code == 200
    res_json = res.json()
    assert "id" in res_json and "email" in res_json and "name" in res_json

