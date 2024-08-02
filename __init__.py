from flask import Flask, request, jsonify
from database import load_game_data
from api import api_blueprint
from flask_swagger_ui import get_swaggerui_blueprint


def create_app():
    app = Flask(__name__)
    load_game_data("scores.jsonl")
    app.register_blueprint(api_blueprint)
    SWAGGER_URL = '/swagger'

    API_URL = '/static/swagger.yaml'

    swaggerui_blueprint = get_swaggerui_blueprint(
        SWAGGER_URL,
        API_URL,
    )

    app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)
    return app
