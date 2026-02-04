def test_health(client):
    res = client.get("/")
    assert res.status_code == 200
