PAYLOAD = {
    "brand": "Marca",
    "model": "Modelo A",
    "weight_g": 60,
    "connection": "wired",
    "polling_rate_hz": 1000,
}


def create(client, **overrides):
    return client.post("/mice", json={**PAYLOAD, **overrides})


def test_create_mouse(client):
    r = create(client)
    assert r.status_code == 201
    body = r.json()
    assert body["id"] > 0
    assert body["brand"] == "Marca"


def test_duplicate_returns_409(client):
    create(client)
    assert create(client).status_code == 409


def test_get_not_found(client):
    assert client.get("/mice/999").status_code == 404


def test_invalid_weight_returns_422(client):
    assert create(client, weight_g=-5).status_code == 422


def test_patch_updates_only_sent_fields(client):
    mouse_id = create(client).json()["id"]
    r = client.patch(f"/mice/{mouse_id}", json={"weight_g": 55})
    assert r.status_code == 200
    assert r.json()["weight_g"] == 55
    assert r.json()["brand"] == "Marca"


def test_delete(client):
    mouse_id = create(client).json()["id"]
    assert client.delete(f"/mice/{mouse_id}").status_code == 204
    assert client.get(f"/mice/{mouse_id}").status_code == 404


def test_search_and_pagination(client):
    create(client, model="Alfa")
    create(client, model="Beta")
    create(client, model="Gama")
    assert len(client.get("/mice?q=alf").json()) == 1
    assert len(client.get("/mice?skip=1&limit=1").json()) == 1