from backend.app import app

def test_home_page():
    client = app.test_client()
    response = client.get('/')
    assert response.status_code == 200

def test_get_expenses():
    client = app.test_client()
    response = client.get('/api/expenses')
    assert response.status_code == 200