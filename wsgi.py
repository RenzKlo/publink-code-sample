"""
WSGI entry point for production deployment.
Used by Gunicorn and other WSGI servers.
"""

import os
from app_new import create_app

# Create the application instance
config_name = os.getenv('FLASK_ENV', 'production')
application = create_app(config_name)

if __name__ == "__main__":
    application.run()
