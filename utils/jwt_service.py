"""
JWT Token Service for secure authentication
"""
import jwt
import logging
from datetime import datetime, timedelta, timezone
from flask import current_app
from functools import wraps


class JWTService:
    """Service for handling JWT tokens securely."""
    
    @staticmethod
    def generate_tokens(user_data):
        """Generate access and refresh tokens for user."""
        try:
            # Current time
            now = datetime.now(timezone.utc)
            
            # Access token payload
            access_payload = {
                'sub': user_data['google_id'],
                'email': user_data['email'],
                'name': user_data['name'],
                'iat': now,
                'exp': now + current_app.config['JWT_ACCESS_TOKEN_EXPIRES'],
                'type': 'access'
            }
            
            # Refresh token payload
            refresh_payload = {
                'sub': user_data['google_id'],
                'iat': now,
                'exp': now + current_app.config['JWT_REFRESH_TOKEN_EXPIRES'],
                'type': 'refresh'
            }
            
            # Generate tokens
            access_token = jwt.encode(
                access_payload,
                current_app.config['JWT_SECRET_KEY'],
                algorithm='HS256'
            )
            
            refresh_token = jwt.encode(
                refresh_payload,
                current_app.config['JWT_SECRET_KEY'],
                algorithm='HS256'
            )
            
            return {
                'access_token': access_token,
                'refresh_token': refresh_token,
                'expires_in': current_app.config['JWT_ACCESS_TOKEN_EXPIRES'].total_seconds()
            }
            
        except Exception as e:
            logging.error(f"Error generating tokens: {str(e)}")
            return None
    
    @staticmethod
    def verify_token(token, token_type='access'):
        """Verify and decode JWT token."""
        try:
            payload = jwt.decode(
                token,
                current_app.config['JWT_SECRET_KEY'],
                algorithms=['HS256']
            )
            
            # Check token type
            if payload.get('type') != token_type:
                return None
                
            return payload
            
        except jwt.ExpiredSignatureError:
            logging.warning("Token has expired")
            return None
        except jwt.InvalidTokenError as e:
            logging.warning(f"Invalid token: {str(e)}")
            return None
    
    @staticmethod
    def refresh_access_token(refresh_token):
        """Generate new access token from refresh token."""
        try:
            # Verify refresh token
            payload = JWTService.verify_token(refresh_token, 'refresh')
            if not payload:
                return None
            
            # Get user data from database
            mongo = current_app.extensions['pymongo']
            user = mongo.db.users.find_one({"google_id": payload['sub']})
            
            if not user:
                return None
            
            # Generate new access token
            user_data = {
                'google_id': user['google_id'],
                'email': user['email'],
                'name': user['name']
            }
            
            tokens = JWTService.generate_tokens(user_data)
            return tokens['access_token'] if tokens else None
            
        except Exception as e:
            logging.error(f"Error refreshing token: {str(e)}")
            return None


def jwt_required(f):
    """Decorator for protecting routes with JWT authentication."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        from flask import request, jsonify
        
        # Get token from Authorization header
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return jsonify({'error': 'No token provided'}), 401
        
        token = auth_header.split(' ')[1]
        
        # Verify token
        payload = JWTService.verify_token(token)
        if not payload:
            return jsonify({'error': 'Invalid or expired token'}), 401
        
        # Add user info to request
        request.user = payload
        return f(*args, **kwargs)
    
    return decorated_function
