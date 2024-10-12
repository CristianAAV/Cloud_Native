import pytest
from unittest.mock import MagicMock, patch
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


# Test de publicación exitosa
def test_get_ping(client):    
    # Mock responses for external services
    response = client.get('/rf005/posts/ping')

    assert response.status_code == 200
    assert response.json == {"message": "Pong"}


@patch('app.getUsers')
# Test de publicación exitosa
def test_get_publication_not_token(mock_getUsers, client):    
    # Mock responses for external services
    mock_getUsers.return_value.status_code = 403
    response = client.get('/rf005/posts/e90f02f9-69b6-43c2-8a36-aa29adb9bc21', headers={})

    assert response.status_code == 403
    assert response.json['msg'] == "No hay token en la solicitud"

@patch('app.getUsers')
def test_get_publication_bad_token(mock_getUsers, client):    
    # Mock responses for external services
    mock_getUsers.return_value.status_code = 401    
    response = client.get('/rf005/posts/e90f02f9-69b6-43c2-8a36-aa29adb9bc21', headers={"Authorization": "Bearer 7abc6070-f97f-426d-ac0f-e39268935288"})

    assert response.status_code == 401
    assert response.json['msg'] == "El token no es válido o está vencido."


@patch('app.getUsers')
@patch('app.getPosts')
def test_get_publication_not_exists(mock_getPosts, mock_getUsers, client):    
    # Mock responses for external services
    mock_getUsers.return_value.status_code = 200
    mock_getUsers.return_value.json.return_value = {
        "id": "57c3192c-bb34-4df6-b8ad-56929c0cb7b5",
        "expireAt": "2024-09-14T19:16:51.285964",
        "token": "7abc6070-f97f-426d-ac0f-e39268935288"
    }    
    mock_getPosts.return_value.status_code = 404
    mock_getPosts.return_value.json.return_value = {}    
    response = client.get('/rf005/posts/e90f02f9-69b6-43c2-8a36-aa19adb9bc21', headers={"Authorization": "Bearer 7abc6070-f97f-426d-ac0f-e39268935288"})

    assert response.json['msg'] == "La publicación con ese id no existe."
    assert response.status_code == 404

@patch('app.getUsers')
@patch('app.getPosts')
def test_get_publication_user_not_Auth(mock_getPosts, mock_getUsers, client):    
    # Mock responses for external services
    mock_getUsers.return_value.status_code = 200
    mock_getUsers.return_value.json.return_value = {
        "id": "57c3192c-bb34-4df6-b8ad-56929c0cb7b5",
        "expireAt": "2024-09-14T19:16:51.285964",
        "token": "7abc6070-f97f-426d-ac0f-e39268935288"
    }    
    mock_getPosts.return_value.status_code = 200
    mock_getPosts.return_value.json.return_value = {
        "createdAt": "2024-09-14T18:17:42.468333",
        "expireAt": "2024-09-21T00:00:00",
        "id": "e90f02f9-69b6-43c2-8a36-aa29adb9bc21",
        "routeId": "079ec991-5729-45ad-899f-a03326d02465",
        "userId": "57c3192c-bb34-4df6-b8ad-56929c0ab7b5"
    }
    response = client.get('/rf005/posts/e90f02f9-69b6-43c2-8a36-aa19adb9bc21', headers={"Authorization": "Bearer 7abc6070-f97f-426d-ac0f-e39268935288"})

    assert response.json['msg'] == "El usuario no tiene permiso para ver el contenido de esta publicación."
    assert response.status_code == 403



@pytest.fixture
def mock_getUsers():
    with patch('app.getUsers') as mock:
        yield mock

@pytest.fixture
def mock_getPosts():
    with patch('app.getPosts') as mock:
        yield mock

@pytest.fixture
def mock_getRoutes():
    with patch('app.getRoutes') as mock:
        yield mock

@pytest.fixture
def mock_getOffers():
    with patch('app.getOffers') as mock:
        yield mock

@pytest.fixture
def mock_getScores():
    with patch('app.getScores') as mock:
        yield mock

def test_get_publication_success(mock_getUsers, mock_getPosts, mock_getRoutes, mock_getOffers, mock_getScores, client):
    # Configura cada mock por separado
    mock_getUsers.return_value = MagicMock(status_code=200, json=lambda: {
        "id": "57c3192c-bb34-4df6-b8ad-56929c0cb7b5",
        "expireAt": "2024-09-14T19:16:51.285964",
        "token": "7abc6070-f97f-426d-ac0f-e39268935288"
    })

    mock_getPosts.return_value = MagicMock(status_code=200, json=lambda: {
        "createdAt": "2024-09-14T18:17:42.468333",
        "expireAt": "2024-09-21T00:00:00",
        "id": "e90f02f9-69b6-43c2-8a36-aa29adb9bc21",
        "routeId": "079ec991-5729-45ad-899f-a03326d02465",
        "userId": "57c3192c-bb34-4df6-b8ad-56929c0cb7b5"
    })

    mock_getRoutes.return_value = MagicMock(status_code=200, json=lambda: {
        "flightId": "FL12345",
        "sourceAirportCode": "JFK",
        "sourceCountry": "USA",
        "destinyAirportCode": "LAX",
        "destinyCountry": "USA",
        "bagCost": 30.00,
        "plannedStartDate": "2024-09-15T08:00:00",
        "plannedEndDate": "2024-09-21T20:00:00",
        "id": "079ec991-5729-45ad-899f-a03326d02465"
    })

    mock_getOffers.return_value = MagicMock(status_code=200, json=lambda: [
        {
            "id": "offer_id",
            "userId": "57c3192c-bb34-4df6-b8ad-56929c0cb7b5",
            "description": "Offer description",
            "size": "SMALL",
            "fragile": False,
            "offer": 675,
            "createdAt": "0001-01-01T00:00:00Z"
        }
    ])

    mock_getScores.return_value = MagicMock(status_code=200, json=lambda: {
        "utility": 5000.0
    })

    response = client.get('/rf005/posts/e90f02f9-69b6-43c2-8a36-aa29adb9bc21',
                          headers={"Authorization": "Bearer 7abc6070-f97f-426d-ac0f-e39268935288"})

    assert response.status_code == 200
    assert response.json['data']['id'] == "e90f02f9-69b6-43c2-8a36-aa29adb9bc21"