from flask import Flask, jsonify, request, Blueprint
from ..commands.create_score import CreateScore
from ..commands.get_score import GetScore
from ..commands.token_authentication import TokenAuthentication
from ..commands.reset import Reset

scores_blueprint = Blueprint('scores', __name__)

@scores_blueprint.route('/scores', methods = ['POST'])
def create():
    TokenAuthentication(auth_token()).execute()

    route = CreateScore(request.get_json()).execute()
    return jsonify(route), 201

@scores_blueprint.route('/scores/offer/<id>', methods = ['GET'])
def of_offer(id):
    TokenAuthentication(auth_token()).execute()

    route = GetScore(id).execute()
    return jsonify(route)

@scores_blueprint.route('/scores/ping', methods = ['GET'])
def ping():
    return 'pong'

@scores_blueprint.route('/scores/reset', methods = ['POST'])
def reset():
    Reset().execute()
    return jsonify({'status': 'OK'})

def auth_token():
    if 'Authorization' in request.headers:
        authorization = request.headers['Authorization']
    else:
        authorization = None
    return authorization