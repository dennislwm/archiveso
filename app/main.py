from flask import Flask

def create_app():
    app = Flask(__name__)
    
    @app.route("/")
    def root():
      return "App-version: 0.1.0"

    return app

app = create_app()