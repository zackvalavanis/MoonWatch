from app.main import app
from fastapi.testclient import TestClient

client = TestClient(app)


def test_watchlist_requires_auth():
    response = client.get("/main/watchlist")
    assert response.status_code == 401
