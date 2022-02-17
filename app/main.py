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
    BLN_APP_DEBUG = os.getenv('APP_DEBUG', False)
    ARCHIVEBOX_PATH = os.getenv('ARCHIVEBOX', './')
    ab = clsArchiveso(ARCHIVEBOX_PATH)
    if (BLN_APP_DEBUG):
        print("DEBUG MODE: " + str(BLN_APP_DEBUG))

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

    #--------------
    # request docs: https://flask.palletsprojects.com/en/2.0.x/api/#flask.Request
    #   args: the key/value pairs in the URL query string
    #   form: the key/value pairs in the body of the request
    #   json: the JSON object in the body of the request, must have application/json
    #   data: the raw data in the body of the request
    # ALL of these are MultiDict instances (except for json). You can access values using:
    #   request.args['key']: use index if you know key exists
    #   request.args.get('key'): use get if key might not exist
    #   request.args.getlist('key'): use getlist if key is sent multiple times, returns the first value
    @app.route("/api/archiveso", methods = ['POST'])
    @auth.login_required
    def post_url():
        strForm = request.form.get('url')
        if (BLN_APP_DEBUG):
            print("strForm: ", strForm)
        if not strForm:
            jsnData = request.data
            strData = json.loads(jsnData)['url']
            if (BLN_APP_DEBUG):
                print("strData: ", strData)
            strUrl = strData
        else:
            strUrl = strForm
        if not strUrl:
            return "Empty strUrl", 400
        return ab.add_url(strUrl)

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=8080)