import pytest
from unittest.mock import patch
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

# Test de publicación exitosa
@patch('app.check_auth')
@patch('app.requests.get')
@patch('app.requests.post')
def test_create_publication_success(mock_post, mock_get, mock_check_auth, client):
    mock_check_auth.return_value = True
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = []
    mock_post.return_value.status_code = 201
    mock_post.return_value.json.return_value = {
        "id": "123", "userId": "user1", "createdAt": "2024-01-01T00:00:00Z"
    }
    
    response = client.post('/rf003/posts', json={
        "flightId": "FL123",
        "expireAt": "2024-11-10T00:00:00Z",
        "plannedStartDate": "2024-12-01T00:00:00Z",
        "plannedEndDate": "2024-12-31T00:00:00Z",
        "origin": {"airportCode": "ABC", "country": "CountryA"},
        "destiny": {"airportCode": "XYZ", "country": "CountryB"},
        "bagCost": 100
    }, headers={"Authorization": "Bearer token"})

    assert response.status_code == 201
    assert response.json['msg'] == "Publicación creada exitosamente"

# Test de fallo de autenticación
@patch('app.check_auth')
@patch('app.requests.get')
def test_create_publication_auth_failure(mock_get, mock_check_auth, client):
    mock_check_auth.return_value = False

    response = client.post('/rf003/posts', json={
        "flightId": "FL123",
        "expireAt": "2025-01-01T00:00:00Z",
    }, headers={"Authorization": "Bearer invalid_token"})

    assert response.status_code == 401
    assert response.json == {"error": "Invalid token"}

# Test de campos faltantes
@patch('app.check_auth')
@patch('app.requests.get')
def test_create_publication_missing_fields(mock_get, mock_check_auth, client):
    mock_check_auth.return_value = True

    response = client.post('/rf003/posts', json={}, headers={"Authorization": "Bearer token"})

    assert response.status_code == 400
    assert response.json == {"error": "Missing required fields"}

# Test de fecha inválida
@patch('app.check_auth')
@patch('app.requests.get')
def test_create_publication_invalid_date(mock_get, mock_check_auth, client):
    mock_check_auth.return_value = True

    response = client.post('/rf003/posts', json={
        "flightId": "FL123",
        "expireAt": "invalid_date",
        "plannedStartDate": "2024-12-01T00:00:00Z",
        "plannedEndDate": "2024-12-31T00:00:00Z",
        "origin": {"airportCode": "ABC", "country": "CountryA"},
        "destiny": {"airportCode": "XYZ", "country": "CountryB"},
        "bagCost": 100
    }, headers={"Authorization": "Bearer token"})

    assert response.status_code == 412
    assert response.json == {'msg': 'Fechas no válidas'}

# Test de token no proporcionado
@patch('app.check_auth')
def test_create_publication_no_token(mock_check_auth, client):
    mock_check_auth.return_value = False

    response = client.post('/rf003/posts', json={
        "flightId": "FL123",
        "expireAt": "2025-01-01T00:00:00Z"
    })

    assert response.status_code == 403
    assert response.json == {"error": "Token not provided"}

# Test de token inválido
@patch('app.check_auth')
def test_create_publication_invalid_token(mock_check_auth, client):
    mock_check_auth.return_value = False

    response = client.post('/rf003/posts', json={
        "flightId": "FL123",
        "expireAt": "2025-01-01T00:00:00Z"
    }, headers={"Authorization": "Bearer invalid_token"})

    assert response.status_code == 401
    assert response.json == {"error": "Invalid token"}

# Test de fechas incorrectas
@patch('app.check_auth')
@patch('app.requests.get')
def test_create_publication_invalid_dates(mock_get, mock_check_auth, client):
    mock_check_auth.return_value = True

    response = client.post('/rf003/posts', json={
        "flightId": "FL123",
        "expireAt": "2025-01-01T00:00:00Z",
        "plannedStartDate": "2025-01-02T00:00:00Z",
        "plannedEndDate": "2025-01-01T00:00:00Z",  # End date before start date
        "origin": {"airportCode": "ABC", "country": "CountryA"},
        "destiny": {"airportCode": "XYZ", "country": "CountryB"},
        "bagCost": 100
    }, headers={"Authorization": "Bearer token"})

    assert response.status_code == 412
    assert response.json == {"msg": "Las fechas del trayecto no son válidas"}

# Test de ruta no encontrada
@patch('app.check_auth')
@patch('app.requests.get')
@patch('app.requests.post')
def test_create_publication_route_not_found(mock_post, mock_get, mock_check_auth, client):
    mock_check_auth.return_value = True
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = []
    mock_post.return_value.status_code = 404  # Simulando que la ruta no se encuentra

    response = client.post('/rf003/posts', json={
        "flightId": "FL123",
        "expireAt": "2024-11-10T00:00:00Z",
        "plannedStartDate": "2024-12-01T00:00:00Z",
        "plannedEndDate": "2024-12-31T00:00:00Z",
        "origin": {"airportCode": "ABC", "country": "CountryA"},
        "destiny": {"airportCode": "XYZ", "country": "CountryB"},
        "bagCost": 100
    }, headers={"Authorization": "Bearer token"})

    assert response.status_code == 500
    assert response.json == {"error": "Failed to create or fetch route"}


@patch('app.check_auth')
@patch('app.requests.get')
def test_create_publication_get_exception(mock_get, mock_check_auth, client):
    mock_check_auth.return_value = True
    mock_get.side_effect = Exception("Error en la solicitud GET")

    response = client.post('/rf003/posts3', json={
        "flightId": "FL123",
        "expireAt": "2025-01-01T00:00:00Z"
    }, headers={"Authorization": "Bearer token"})

    assert response.status_code == 404

@patch('app.check_auth')
@patch('app.requests.get')
@patch('app.requests.post')
def test_create_publication_response_content(mock_post, mock_get, mock_check_auth, client):
    mock_check_auth.return_value = True
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = []
    mock_post.return_value.status_code = 201
    mock_post.return_value.json.return_value = {
        "id": "123", "userId": "user1", "createdAt": "2024-01-01T00:00:00Z"
    }
    
    response = client.post('/rf003/posts', json={
        "flightId": "FL123",
        "expireAt": "2024-11-28T00:00:00Z",
        "plannedStartDate": "2024-12-01T00:00:00Z",
        "plannedEndDate": "2024-12-31T00:00:00Z",
        "origin": {"airportCode": "ABC", "country": "CountryA"},
        "destiny": {"airportCode": "XYZ", "country": "CountryB"},
        "bagCost": 100
    }, headers={"Authorization": "Bearer token"})

    print(response.json)
    assert response.status_code == 201
    assert response.json['data']['id'] == "123"
    assert response.json['data']['userId'] == "user1"
    assert response.json['data']['createdAt'] == "2024-01-01T00:00:00Z"
