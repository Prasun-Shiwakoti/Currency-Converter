from fastapi.testclient import TestClient
from app.main import app


client = TestClient(app)

def test_convert_valid():
    response = client.get("/convert?from_currency=USD&to_currency=EUR&amount=100")
    assert response.status_code == 200
    data = response.json()
    assert data["from"] == "USD" # Check if source currency is correctly sent
    assert data["to"] == "EUR" # Check if target currency is correctly sent
    assert data["amount"] == 100 # Check if amount is correctly sent
    assert "converted_amount" in data # Check if converted amount is present which indicates successful conversion
    assert isinstance(data["converted_amount"], float) # Check if converted amount is a float
