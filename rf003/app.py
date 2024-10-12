from flask import Flask, request, jsonify
import requests
from datetime import datetime, timezone
import os

app = Flask(__name__)

# URLs de los endpoints
ROUTES_PATH = os.environ.get('ROUTES_PATH', 'http://localhost:3002')
POSTS_PATH = os.environ.get('POSTS_PATH', 'http://localhost:3001')
USERS_PATH = os.environ.get('USERS_PATH', 'http://localhost:3000')

ROUTES_URL = ROUTES_PATH + '/routes'
POSTS_URL = POSTS_PATH + '/posts'
AUTH_URL = USERS_PATH + '/users/me'

# Función para verificar autenticación
def check_auth(token):
    response = requests.get(AUTH_URL, headers={'Authorization': f'Bearer {token}'})
    return response.status_code == 200

# Función para verificar si el usuario ya tiene una publicación
def user_has_existing_post(route_id, token):
    post_check_url = f'{POSTS_URL}?expire=false&route={route_id}&owner=me'
    response = requests.get(post_check_url, headers={'Authorization': f'Bearer {token}'})
    return response.status_code == 200 and len(response.json()) > 0

# Función para crear una nueva ruta si no existe
def create_route_if_not_exists(flight_id, origin, destiny, bag_cost, planned_start_date, planned_end_date, token):
    response = requests.get(f'{ROUTES_URL}?flight={flight_id}', headers={'Authorization': f'Bearer {token}'})
    if response.status_code == 200 and len(response.json()) > 0:
        route = response.json()
        return route[0]['id'], route[0]['createdAt']
    elif response.status_code == 200 and len(response.json()) == 0:
        route_data = {
            "flightId": flight_id,
            "sourceAirportCode": origin['airportCode'],
            "sourceCountry": origin['country'],
            "destinyAirportCode": destiny['airportCode'],
            "destinyCountry": destiny['country'],
            "bagCost": bag_cost,
            "plannedStartDate": planned_start_date,
            "plannedEndDate": planned_end_date
        }
        response = requests.post(ROUTES_URL, json=route_data, headers={'Authorization': f'Bearer {token}'})
        if response.status_code == 201:
            route = response.json()
            return route['id'], route['createdAt']
    return None, None

@app.route('/rf003/posts/ping', methods=['GET'])
def ping():
    return jsonify(message="Pong"), 200

@app.route('/rf003/posts', methods=['POST'])
def create_publication():
    data = request.get_json()
    token = request.headers.get('Authorization')
    
    if not token or not token.startswith('Bearer '):
        return jsonify({"error": "Token not provided"}), 403
    
    token = token[len('Bearer '):]
    if not check_auth(token):
        return jsonify({"error": "Invalid token"}), 401

    flight_id = data.get('flightId')
    expire_at = data.get('expireAt')
    planned_start_date = data.get('plannedStartDate')
    planned_end_date = data.get('plannedEndDate')
    origin = data.get('origin')
    destiny = data.get('destiny')
    bag_cost = data.get('bagCost')

    if not flight_id or not expire_at or not planned_start_date or not planned_end_date or not origin or not destiny or bag_cost is None:
        return jsonify({"error": "Missing required fields"}), 400
    
    try:
        expire_at = datetime.fromisoformat(expire_at)
        _planned_start_date = datetime.fromisoformat(planned_start_date)
        _planned_end_date = datetime.fromisoformat(planned_end_date)
        _now = datetime.utcnow().replace(tzinfo=timezone.utc)

        # Validaciones adicionales
        if _planned_start_date <= _now:
            return jsonify({"msg": "Las fechas del trayecto no son válidas"}), 412
        if _planned_end_date <= _planned_start_date:
            return jsonify({"msg": "Las fechas del trayecto no son válidas"}), 412
        if expire_at <= _now or expire_at > _planned_start_date:
            return jsonify({"msg": "La fecha expiración no es válida"}), 412

    except ValueError:
        return jsonify({"msg": "Fechas no válidas"}), 412

    # Crear o encontrar la ruta
    route_id, route_created_at = create_route_if_not_exists(flight_id, origin, destiny, bag_cost, planned_start_date, planned_end_date, token)
    if not route_id:
        return jsonify({"error": "Failed to create or fetch route"}), 500

    # Verificar si el usuario ya tiene una publicación
    if user_has_existing_post(route_id, token):
        return jsonify({"msg": "El usuario ya tiene una publicación para la misma fecha"}), 412

    # Crear publicación - test gitflow
    post_data = {
        "routeId": route_id,
        "expireAt": expire_at.isoformat()
    }
    response = requests.post(POSTS_URL, json=post_data, headers={'Authorization': f'Bearer {token}'})
    
    if response.status_code == 201:
        post = response.json()
        response_data = {
            "data": {
                "id": post['id'],
                "userId": post['userId'],
                "createdAt": post['createdAt'],
                "expireAt": expire_at.isoformat(),
                "route": {
                    "id": route_id,
                    "createdAt": route_created_at
                }
            },
            "msg": "Publicación creada exitosamente"
        }
        return jsonify(response_data), 201
    elif response.status_code == 412:
        return jsonify(response.json()), 412
    else:
        return jsonify({"error": "Failed to create post"}), response.status_code

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=3013)
