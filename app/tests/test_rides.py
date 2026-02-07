def test_create_ride_unauthorized(client):
    res = client.post(
        "/rides/",
        json={"distance": 100, "duration": 45, "city": "BLR"},
    )
    assert res.status_code in [401, 403]


def test_create_ride_authorized(client, auth_headers):
    res = client.post(
        "/rides/",
        json={"distance": 100, "duration": 45, "city": "BLR"},
        headers=auth_headers,
    )
    assert res.status_code in [200, 201]
    res_json = res.json()
    assert "id" in res_json
    assert "distance" in res_json
    assert "duration" in res_json
    assert "created_at" in res_json


def test_list_rides_unauthorized(client):
    res = client.get("/rides/")
    assert res.status_code in [401, 403]


def test_list_rides_only_own_rides(client, test_user, auth_headers):
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

    res_ride_test_user = client.post(
        "/rides/",
        json={"distance": 100, "duration": 45, "city": "BLR"},
        headers=auth_headers,
    )
    res_ride_test_user1 = client.post(
        "/rides/",
        json={"distance": 400, "duration": 1450, "city": "Mysore"},
        headers=token_user1,
    )
    res_get_ride_user = client.get("/rides/", headers=auth_headers)
    assert res_get_ride_user.status_code in [200, 201]
    assert not "Mysore" in [item.get("city") for item in res_get_ride_user.json()]


def test_list_rides_pagination(client, auth_headers):
    [
        client.post("/rides/", json=item, headers=auth_headers)
        for item in [
            {"distance": 400, "duration": 1450, "city": "Mysore"},
            {"distance": 100, "duration": 45, "city": "BLR"},
            {"distance": 200, "duration": 145, "city": "DEL"},
            {"distance": 300, "duration": 245, "city": "MUM"},
            {"distance": 450, "duration": 345, "city": "CHN"},
            {"distance": 500, "duration": 445, "city": "HYD"},
            {"distance": 600, "duration": 545, "city": "CCU"},
            {"distance": 700, "duration": 645, "city": "PPT"},
        ]
    ]
    res1 = client.get("/rides?limit=2&offset=0", headers=auth_headers)
    res2 = client.get("/rides?limit=2&offset=2", headers=auth_headers)
    assert len(res1.json()) == 2
    assert len(res2.json()) == 2
    assert not res1.json() == res2.json()


def test_list_rides_ordering(client, auth_headers):
    [
        client.post("/rides/", json=item, headers=auth_headers)
        for item in [
            {"distance": 400, "duration": 1450, "city": "Mysore"},
            {"distance": 100, "duration": 45, "city": "BLR"},
            {"distance": 200, "duration": 145, "city": "DEL"},
            {"distance": 300, "duration": 245, "city": "MUM"},
            {"distance": 450, "duration": 345, "city": "CHN"},
            {"distance": 500, "duration": 445, "city": "HYD"},
            {"distance": 600, "duration": 545, "city": "CCU"},
            {"distance": 700, "duration": 645, "city": "PPT"},
        ]
    ]
    res = client.get("/rides?order_by=distance&order=asc", headers=auth_headers)
    res_json = res.json()
    assert (
        res_json[0]["distance"]
        >= res_json[1]["distance"]
        >= res_json[2]["distance"]
        >= res_json[3]["distance"]
    )
