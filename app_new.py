"""
PubLink Flask Application Factory

This module creates the Flask application instance for production deployment.
Used by Gunicorn and other WSGI servers.
"""

import os
from flask import Flask
from flask_pymongo import PyMongo
import logging
import pytz

# Global extensions
mongo = PyMongo()

def create_app(config_name=None):
    """
    Application factory function
    """
    if config_name is None:
        config_name = os.getenv('FLASK_ENV', 'development')
    
    app = Flask(__name__)
    
    # Load configuration
    from config import config
    app.config.from_object(config[config_name])
    
    # Initialize extensions
    mongo.init_app(app)
    
    # Initialize security extensions
    from flask_cors import CORS
    from flask_limiter import Limiter
    from flask_limiter.util import get_remote_address
    
    # Configure CORS
    CORS(app, origins=app.config['CORS_ORIGINS'])
    
    # Configure rate limiting
    limiter = Limiter(
        app=app,
        key_func=get_remote_address,
        default_limits=["100 per hour", "20 per minute"]
    )
    
    # Add security headers
    @app.after_request
    def add_security_headers(response):
        for header, value in app.config['SECURITY_HEADERS'].items():
            response.headers[header] = value
        return response
    
    # Store mongo in app extensions for easier access
    app.extensions['pymongo'] = mongo
    
    # Register blueprints
    from routes.main import main_bp
    from routes.auth import auth_bp
    from routes.routes import routes_bp
    from routes.pois import pois_bp
    
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)  # Prefix: /auth
    app.register_blueprint(routes_bp)  # Prefix: /api/routes
    app.register_blueprint(pois_bp)  # Prefix: /api/pois
    
    # Register error handlers
    from utils.error_handlers import register_error_handlers
    register_error_handlers(app)
    
    # Set up logging
    if not app.debug and not app.testing:
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s %(levelname)s: %(message)s'
        )
    
    return app

# For WSGI servers, they will call create_app() directly
# Only create app instance if this file is run directly
if __name__ == '__main__':
    # Determine the configuration to use
    config_name = os.getenv('FLASK_ENV', 'development')
    app = create_app(config_name)
    app.run(host='0.0.0.0', port=5000)

# This is what Gunicorn will use
if __name__ == "__main__":
    # This should only run in development
    app.run(debug=False, host='0.0.0.0', port=5000)
