import os
import json

from flask import Flask, request
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash
from clsArchiveso import clsArchiveso

def create_app():
    app = Flask(__name__)
    auth = HTTPBasicAuth()

    API_USERNAME = os.getenv('LOWDEFY_SECRET_API_USERNAME', '')
    API_PASSWORD = os.getenv('LOWDEFY_SECRET_API_PASSWORD', '')
    ARCHIVEBOX_PATH = os.getenv('ARCHIVEBOX', './')
    ab = clsArchiveso(ARCHIVEBOX_PATH)

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
        return "App-version: " + ab.get_version() + " | CLI-version: " + ab.get_cli_version()

    @app.route("/api/archiveso", methods = ['POST'])
    @auth.login_required
    def post_url():
        jsnData = request.data
        strUrl = json.loads(jsnData)['url']
        if not strUrl:
            return "Empty strUrl", 400
        return ab.add_url(strUrl)

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=8080)