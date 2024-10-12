from dotenv import load_dotenv
loaded = load_dotenv('.env.development')

from flask import Flask, jsonify
from .session import engine
from .models.model import Base
from .blueprints.scores import scores_blueprint
from .errors.errors import ApiError

app = Flask(__name__)
app.register_blueprint(scores_blueprint)

Base.metadata.create_all(engine)

@app.errorhandler(ApiError)
def handle_exception(err):
    response = {
      "mensaje": err.description 
    }
    return jsonify(response), err.code
