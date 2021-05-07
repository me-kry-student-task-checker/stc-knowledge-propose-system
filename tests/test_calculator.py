def test_add(client):
    response = client.post("/calc/", json={"numberA": 30, "numberB": 5, "operation": "add"})
    assert response.json["result"] == 35


def test_minus(client):
    response = client.post("/calc/", json={"numberA": 30, "numberB": 5, "operation": "minus"})
    assert response.json["result"] == 25


def test_multiple(client):
    response = client.post("/calc/", json={"numberA": 30, "numberB": 5, "operation": "multiple"})
    assert response.json["result"] == 150


def test_divide(client):
    response = client.post("/calc/", json={"numberA": 30, "numberB": 5, "operation": "divide"})
    assert response.json["result"] == 6
