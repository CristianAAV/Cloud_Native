import requests
from flask import Flask, jsonify, request, Blueprint
from ..commands.create_user import CreateUser
from ..commands.generate_token import GenerateToken
from ..commands.get_user import GetUser
from ..commands.reset import Reset
from ..commands.update_user import UpdateUser
from ..commands.update_score import UpdateScore
from ..session import Session
from ..models.user import User

users_blueprint = Blueprint('users', __name__)

@users_blueprint.route('/users/hook', methods = ['PATCH'])
def hook():
    json = request.get_json()
    #####################    
    url = "https://email-service-441252389525.us-central1.run.app/api/emails/notify-user-verification"
    session = Session()
    userId = json['userIdentifier']
    user = session.query(User).filter_by(id=userId).one()
    userEmail = user.email
    userStatus = json['status']
    userRuv = json['RUV']
    
    data = {
    	"email": userEmail
        , "userStatus": userStatus
        , "RUV": userRuv
    }

    headers = {
        "Content-Type": "application/json"
    }

    response = requests.post(url, json=data, headers=headers)
    # print('-----------------------data-------------------------------')
    # print(userEmail)
    # print(userStatus)
    # print(userRuv)
    #######################
    UpdateScore(json['userIdentifier'], json['score']).execute()
    return jsonify({'msg': 'OK'})

@users_blueprint.route('/users', methods=['POST'])
def create():
    user = CreateUser(request.get_json()).execute()
    return jsonify(user), 201


@users_blueprint.route('/users/<id>', methods=['PATCH'])
def update(id):
    response = UpdateUser(id, request.get_json()).execute()
    return jsonify(response)


@users_blueprint.route('/users/auth', methods=['POST'])
def auth():
    user = GenerateToken(request.get_json()).execute()
    return jsonify(user)


@users_blueprint.route('/users/me', methods=['GET'])
def show():
    user = GetUser(auth_token()).execute()
    return jsonify(user)


@users_blueprint.route('/users/ping', methods=['GET'])
def ping():
    return 'pong'


@users_blueprint.route('/users/reset', methods=['POST'])
def reset():
    Reset().execute()
    return jsonify({'status': 'OK'})


def auth_token():
    if 'Authorization' in request.headers:
        authorization = request.headers['Authorization']
    else:
        authorization = None
    return authorization