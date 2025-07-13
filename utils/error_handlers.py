from flask import jsonify
import logging


def register_error_handlers(app):
    """Register error handlers for the application."""
    
    @app.errorhandler(404)
    def not_found_error(error):
        logging.warning(f"404 error: {error}")
        return jsonify({"error": "Resource not found"}), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        logging.error(f"500 error: {error}")
        return jsonify({"error": "Internal server error"}), 500
    
    @app.errorhandler(400)
    def bad_request_error(error):
        logging.warning(f"400 error: {error}")
        return jsonify({"error": "Bad request"}), 400
    
    @app.errorhandler(401)
    def unauthorized_error(error):
        logging.warning(f"401 error: {error}")
        return jsonify({"error": "Unauthorized"}), 401
    
    @app.errorhandler(403)
    def forbidden_error(error):
        logging.warning(f"403 error: {error}")
        return jsonify({"error": "Forbidden"}), 403
