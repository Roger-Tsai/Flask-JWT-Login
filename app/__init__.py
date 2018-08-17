from flask import Flask, request
from flask_security import Security, SQLAlchemyUserDatastore

from app.database import db

def create_app(config_filename):
    app = Flask(__name__)
    app.config.from_object(config_filename)

    # import database model
    from app.users.model import Users

    db.init_app(app)
    
    with app.app_context():
        db.create_all()

    # Blueprint
    # [User Module]
    from app.users.api import user_bp
    app.register_blueprint(user_bp, url_prefix='/user')

    @app.before_request
    def before_request():
        ip = request.remote_addr
        url = request.url
        
    # [CORS]
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Origin', '*')
        if request.method == 'OPTIONS':
            response.headers['Access-Control-Allow-Methods'] = 'DELETE, GET, POST, PUT'
            headers = request.headers.get('Access-Control-Request-Headers')
            if headers:
                response.headers['Access-Control-Allow-Headers'] = headers
        return response

    return app