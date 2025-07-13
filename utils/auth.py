from functools import wraps
from flask import request, jsonify, current_app
import logging
from google.oauth2 import id_token
from google.auth.transport import requests as google_requests
from datetime import datetime, timedelta
import pytz
from config import Config

tz = pytz.timezone(Config.TIMEZONE)


def store_token_in_db(token, user_info, expires_in):
    """Store authentication token in database."""
    expiration_time = datetime.now(tz) + timedelta(seconds=expires_in)
    current_app.extensions['pymongo'].db.tokens.insert_one({
        "token": token,
        "user_info": user_info,
        "expires_at": expiration_time
    })
    logging.info("Token stored in database with expiration time")


def get_token_from_db(token):
    """Retrieve token information from database."""
    token_data = current_app.extensions['pymongo'].db.tokens.find_one({"token": token})
    if token_data:
        expires_at = token_data["expires_at"]
        if expires_at.tzinfo is None:
            expires_at = expires_at.replace(tzinfo=tz)
        if expires_at > datetime.now(tz):
            logging.info("Token found in database and is valid")
            return token_data["user_info"]
    logging.info("Token not found or expired")
    return None


def auth_middleware(f):
    """Authentication middleware decorator."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        auth_header = request.headers.get("Authorization")
        if not auth_header:
            logging.warning("Authorization token is missing")
            return jsonify({"error": "Authorization token is missing"}), 401

        # Extract the token from the "Bearer" prefix
        parts = auth_header.split()
        if parts[0].lower() != "bearer" or len(parts) != 2:
            logging.warning("Authorization header must start with Bearer")
            return jsonify({"error": "Invalid authorization header"}), 401

        token = parts[1]

        # Check if the token is in the database
        user_info = get_token_from_db(token)
        if not user_info:
            try:
                user_info = id_token.verify_oauth2_token(
                    token, google_requests.Request(), Config.GOOGLE_CLIENT_ID
                )
                # Store the token in the database with its expiration time
                expires_in = user_info.get("exp") - datetime.now(tz).timestamp()
                store_token_in_db(token, user_info, expires_in)
                logging.info("Token verified with Google and stored in database")
            except ValueError as e:
                logging.error(f"Invalid token: {e}")
                return jsonify({"error": "Invalid token", "message": str(e)}), 401
            except Exception as e:
                logging.error(f"Error verifying token: {e}")
                return jsonify({"error": str(e)}), 500

        request.user = user_info
        return f(*args, **kwargs)

    return decorated_function
