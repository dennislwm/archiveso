import os

from flask import Flask
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash

def create_app():
    app = Flask(__name__)
    auth = HTTPBasicAuth()

    API_USERNAME = os.getenv('LOWDEFY_SECRET_API_USERNAME', '')
    API_PASSWORD = os.getenv('LOWDEFY_SECRET_API_PASSWORD', '')

    users = {
        API_USERNAME: generate_password_hash(API_PASSWORD),
    }

    @auth.verify_password
    def verify_password(username, password):
        if username in users:
            return check_password_hash(users.get(username), password)
        return False

    @app.route("/")
    @auth.login_required
    def root():
        return "App-version: 0.2.0"

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=8080)