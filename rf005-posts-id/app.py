from flask import Flask, request, jsonify
import requests
from datetime import datetime, timezone
import os

##from dotenv import load_dotenv, find_dotenv

app = Flask(__name__)

# URLs de los endpoints
USER_URL = os.getenv('USERS_PATH', "http://users:3000")
POSTS_URL = os.getenv('POSTS_PATH', "http://posts:3001")
ROUTES_URL = os.getenv('ROUTES_PATH', "http://routes:3002")
OFFERS_URL = os.getenv('OFFERS_PATH', "http://offers:3003")
SCORES_URL = os.getenv('SCORES_PATH', "http://scores:3012")

@app.route('/rf005/posts/ping', methods=['GET'])
def ping():
    return jsonify(message="Pong"), 200

def getUsers(headers):    
        response_user = requests.get(f'{USER_URL}/users/me', headers=headers)
        return response_user

def getPosts(headers,id):    
        response_posts = requests.get(f'{POSTS_URL}/posts/{id}', headers=headers)
        return response_posts

def getRoutes(headers,route_id):    
        response_routes = requests.get(f'{ROUTES_URL}/routes/{route_id}', headers=headers)
        return response_routes


def getOffers(headers,post_id):    
        response_offers = requests.get(f'{OFFERS_URL}/offers?post={post_id}', headers=headers)
        return response_offers

def getScores(headers,offer_id):    
        response_scores = requests.get(f'{SCORES_URL}/scores/offer/{offer_id}', headers=headers)
        return response_scores


@app.route('/rf005/posts/<id>', methods=['GET'])
def get_publication(id):
    token = request.headers.get('Authorization')
    
    if not token:
            return jsonify({"msg": "No hay token en la solicitud"}), 403
    headers = {'Authorization': token}
    # Verifica si el valor del token es None, vacío, o si la clave no está presente
    try:
        response_user=getUsers(headers)
        response_user.raise_for_status()
        if response_user.status_code == 401:
            print(f"token1: {token}")
            return jsonify({"msg": "El token no es válido o está vencido."}), 401
        if response_user.status_code == 403:
            return jsonify({"msg": "No hay token en la solicitud"}), 403
        data_user = response_user.json()
        user_id = data_user.get('id')
        if not user_id:
            return jsonify({"msg": "El token no es válido o está vencido."}), 401

    except requests.HTTPError as http_err:
        if response_user.status_code == 403:
            return jsonify({"msg": "No hay token en la solicitud"}), 403
        if response_user.status_code == 401:
            print(f"token3: {token}")
            return jsonify({"msg": "El token no es válido o está vencido."}), 401
        raise http_err
    


    try:
        response_posts = getPosts(headers,id)
        if response_posts.status_code == 404:
            return jsonify({"msg": "La publicación con ese id no existe."}), 404
        response_posts.raise_for_status()
        data_posts = response_posts.json()
        post_user_id = data_posts.get('userId')
        post_createdAt = data_posts.get('createdAt')
        post_expireAt = data_posts.get('expireAt')
        post_id = data_posts.get('id')
        route_id = data_posts.get('routeId')
        if (post_user_id != user_id):
            return jsonify({"msg": f"El usuario no tiene permiso para ver el contenido de esta publicación."}), 403
    except requests.HTTPError as http_err:
        if response_posts.status_code == 404:
            return jsonify({"msg": "La publicación con ese id no existe."}), 404
        

    try:
        response_routes = getRoutes(headers,route_id)
        response_routes.raise_for_status()
        data_routes = response_routes.json()
        flightId = data_routes.get('flightId')
        origin_airportCode = data_routes.get('sourceAirportCode')
        origin_country = data_routes.get('sourceCountry')
        destiny_airportCode = data_routes.get('destinyAirportCode')
        destiny_country = data_routes.get('destinyCountry')
        bag_cost = data_routes.get('bagCost')
        planned_start_date = data_routes.get('plannedStartDate')
        planned_end_date = data_routes.get('plannedEndDate')
    except requests.HTTPError as http_err:
        if response_routes.status_code == 404:
            return jsonify({"msg": "No existe el trayecto definido."}), 405

    try:
        # Obtener ofertas
        response_offers = getOffers(headers,post_id)
        response_offers.raise_for_status()
        data_offers = response_offers.json()
        
        offers = []
        
        for offer_data in data_offers:
            offer_id = offer_data.get('id')
            offer_user_id = offer_data.get('userId')
            description = offer_data.get('description')
            size = offer_data.get('size')
            fragile = offer_data.get('fragile')
            offer_value = offer_data.get('offer')
            created_at = offer_data.get('createdAt')
            
            try:
                response_scores = getScores(headers,offer_id)   
                response_scores.raise_for_status()
                data_scores = response_scores.json()
                scores = data_scores.get('utility')
                if not isinstance(scores, (int, float)): 
                    scores = 0  
            except requests.HTTPError as http_err:
                if response_scores.status_code == 404:
                    scores = 0 
                else:
                    return jsonify({"msg": "Error al obtener utilidad."}), 500
            
            offer_dict = {
                "id": offer_id,
                "userId": offer_user_id,
                "description": description,
                "size": size,
                "fragile": fragile,
                "offer": offer_value,
                "score": scores,
                "createdAt": created_at
            }
            offers.append(offer_dict)
        
            offers_sorted = sorted(offers, key=lambda x: x['score'], reverse=True)
           
    except requests.HTTPError as http_err:
        if response_routes.status_code == 404:
            return jsonify({"msg": "No existen ofertas."}), 405

    response_data =    {
            "data": {
                "id": post_id,
                "expireAt": post_expireAt,
                "route": {
                    "id": route_id,
                    "flightId": flightId,
                    "origin": {
                        "airportCode": origin_airportCode,
                        "country": origin_country
                    },
                    "destiny": {
                        "airportCode": destiny_airportCode,
                        "country": destiny_country
                    },
                    "bagCost": bag_cost
                },
                "plannedStartDate": planned_start_date,
                "plannedEndDate": planned_end_date,
                "createdAt": post_createdAt,
                "offers": offers_sorted
            }
        }

    return jsonify(response_data), 200


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=3007)