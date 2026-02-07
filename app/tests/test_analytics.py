def test_analytics_unauthorized(client):
    res = client.get("/rides/analytics")
    assert res.status_code == 401


def test_analytics_no_rides(client, auth_headers):
    res = client.get("/rides/analytics", headers=auth_headers)
    assert res.status_code == 200
    res_json = res.json()
    assert res_json == {
        "total_rides": 0,
        "total_distance": 0,
        "total_duration": 0,
        "longest_ride": 0,
        "average_distance": 0,
        "last_ride_at": None,
    }


def test_analytics_with_rides(client, auth_headers):
    [
        client.post("/rides/", json=item, headers=auth_headers)
        for item in [
            {"distance": 600, "duration": 1450, "city": "Mysore"},
            {"distance": 100, "duration": 45, "city": "BLR"},
            {"distance": 200, "duration": 145, "city": "DEL"},
        ]
    ]
    res = client.get("/rides/analytics", headers=auth_headers)
    res_json = res.json()
    assert res_json["total_rides"] == 3
    assert res_json["total_distance"] == 900
    assert res_json["longest_ride"] == 600
    assert res_json["average_distance"] == 300
    assert res_json["last_ride_at"] is not None


def test_analytics_only_own_rides(client, auth_headers):
    test_user1 = client.post(
        "/users/",
        json={"email": "user1@example.com", "name": "user1", "password": "user@123"},
    )
    res_test_user1_login = client.post(
        "/users/login",
        json={
            "email": "user1@example.com",
            "password": "user@123",
        },
    )
    token_user1 = {
        "Authorization": f"Bearer {res_test_user1_login.json()['access_token']}"
    }

    [
        client.post("/rides/", json=item, headers=auth_headers)
        for item in [
            {"distance": 600, "duration": 1450, "city": "Mysore"},
            {"distance": 100, "duration": 45, "city": "BLR"},
            {"distance": 200, "duration": 145, "city": "DEL"},
        ]
    ]

    [
        client.post("/rides/", json=item, headers=token_user1)
        for item in [
            {"distance": 300, "duration": 1450, "city": "Managlore"}
        ]
    ]

    res_get_analytics_user = client.get("/rides/", headers=auth_headers)
    assert len(res_get_analytics_user.json()) == 3
