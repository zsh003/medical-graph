from flask import Flask
from app.routes import statistics, graph

def create_app():
    app = Flask(__name__)
    
    return app 