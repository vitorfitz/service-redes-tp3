from flask import Flask, request, jsonify
from database import load_game_data
from api import api_blueprint


def create_app():
    app = Flask(__name__)
    load_game_data("scores.jsonl")
    app.register_blueprint(api_blueprint)
    return app
