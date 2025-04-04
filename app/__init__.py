from flask import Flask
from flask_jwt_extended import JWTManager
from flask_swagger_ui import get_swaggerui_blueprint
from flask_cors import CORS

from .config import Config
from .database import db

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    jwt = JWTManager(app)
    
    # Enable CORS
    CORS(app)
    # Initialize database
    db.init_app(app)
    
   # push context manually to app
    with app.app_context():
        db.create_all()
    
     
    # Register Blueprints

    

    # Swagger setup
    SWAGGER_URL = '/swagger'
    API_URL = '/static/swagger.json'
    swaggerui_blueprint = get_swaggerui_blueprint(SWAGGER_URL, API_URL, config={'app_name': "API ADRES"})
    app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

    return app