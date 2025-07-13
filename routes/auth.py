from flask import Blueprint, request, jsonify, current_app
from google.oauth2 import id_token
from google.auth.transport import requests as google_requests
import logging
from datetime import datetime
import pytz
from utils.auth import store_token_in_db
from utils.jwt_service import JWTService
from config import Config

# Import mongo from the app context - will be available when app is created
from flask import current_app

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

tz = pytz.timezone(Config.TIMEZONE)


@auth_bp.route('/google', methods=['POST'])
def google_auth():
    """Handle Google OAuth authentication."""
    data = request.json
    token = data.get("token")

    if not token:
        logging.warning("Token is required")
        return jsonify({"error": "Token is required"}), 400

    try:
        # Verify the token with Google
        user_info = id_token.verify_oauth2_token(
            token, google_requests.Request(), Config.GOOGLE_CLIENT_ID
        )
        logging.info("Token verified with Google")
        
        # Get user data
        user_id = user_info["sub"]
        email = user_info["email"]
        name = user_info["name"]
        profile_image = user_info["picture"]

        # Check if the user already exists
        existing_user = current_app.extensions['pymongo'].db.users.find_one({"google_id": user_id})

        if existing_user:
            # If user exists, prepare user data
            user_data = {
                "google_id": existing_user["google_id"],
                "name": existing_user["name"],
                "email": existing_user["email"],
                "profile_image": existing_user["profile_image"],
            }
            logging.info("Existing user found")
        else:
            # If user does not exist, create a new user
            new_user = {
                "google_id": user_id,
                "name": name,
                "email": email,
                "profile_image": profile_image,
                "created_at": datetime.now(tz)
            }
            current_app.extensions['pymongo'].db.users.insert_one(new_user)
            user_data = {
                "google_id": str(new_user["google_id"]),
                "name": new_user["name"],
                "email": new_user["email"],
                "profile_image": new_user["profile_image"],
            }
            logging.info("New user created")

        # Generate JWT tokens
        tokens = JWTService.generate_tokens(user_data)
        if not tokens:
            return jsonify({"error": "Failed to generate authentication tokens"}), 500

        # Store the token for future use (legacy)
        expires_in = user_info.get("exp") - datetime.now(tz).timestamp()
        store_token_in_db(token, user_info, expires_in)

        # Return user data with JWT tokens
        response_data = {
            "user": {
                "id": user_data["google_id"],
                "name": user_data["name"],
                "email": user_data["email"],
                "profileImage": user_data["profile_image"],
            },
            "access_token": tokens["access_token"],
            "refresh_token": tokens["refresh_token"],
            "expires_in": tokens["expires_in"]
        }

        return jsonify(response_data), 200

    except ValueError as e:
        logging.error(f"Invalid token: {e}")
        return jsonify({"error": "Invalid token", "message": str(e)}), 401


@auth_bp.route('/refresh', methods=['POST'])
def refresh_token():
    """Refresh access token using refresh token."""
    data = request.json
    refresh_token = data.get("refresh_token")

    if not refresh_token:
        logging.warning("Refresh token is required")
        return jsonify({"error": "Refresh token is required"}), 400

    try:
        # Generate new access token
        new_access_token = JWTService.refresh_access_token(refresh_token)
        
        if not new_access_token:
            return jsonify({"error": "Invalid or expired refresh token"}), 401

        return jsonify({
            "access_token": new_access_token,
            "token_type": "Bearer"
        }), 200

    except Exception as e:
        logging.error(f"Token refresh failed: {e}")
        return jsonify({"error": "Token refresh failed"}), 500


@auth_bp.route('/test-token', methods=['POST'])
def generate_test_token():
    """Generate a test JWT token for development purposes."""
    data = request.json
    user_id = data.get("user_id", "test_user")
    
    try:
        # Create mock user data for token generation
        user_data = {
            'google_id': user_id,
            'email': f'{user_id}@test.com',
            'name': f'Test User {user_id}'
        }
        
        tokens = JWTService.generate_tokens(user_data)
        
        return jsonify({
            "access_token": tokens["access_token"],
            "refresh_token": tokens["refresh_token"],
            "user_id": user_id,
            "token_type": "Bearer"
        }), 200
        
    except Exception as e:
        logging.error(f"Test token generation failed: {e}")
        return jsonify({"error": "Test token generation failed"}), 500
