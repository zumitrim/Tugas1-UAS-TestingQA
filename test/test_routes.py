import json

from .settings import DEFAULT_PRICE

def test_product_detail_api(client):
    id = 3
    response = client.get(f"/api/products/{id}")
    assert response.status_code == 200
    data = json.loads(response.data)
    assert id == data.get('id')
    assert DEFAULT_PRICE * id


def test_product_api(client):
    response = client.get("/api/products")
    print(response.status_code)
    assert response.status_code == 200

def test_post_cart(client):
    
    cart_data = {
        "coupon_code": "TEST123",
        "shipping_fee": 5.0,
        "cart_items": [
            {"product_id": 1, "qty": 2},
            {"product_id": 2, "qty": 3}
        ]
    }

    response = client.post("/api/cart", json=cart_data)
    assert response.status_code == 200
    assert response.data.decode("utf-8") == "data created"

