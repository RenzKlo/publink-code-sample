import logging
from datetime import datetime
import pytz
from flask import current_app
from config import Config

tz = pytz.timezone(Config.TIMEZONE)


class UserService:
    """Service class for handling user-related operations."""
    
    def __init__(self):
        self.mongo = None  # Will use current_app.extensions['pymongo'] when needed
    
    def create_user(self, user_data):
        """Create a new user."""
        user_data['created_at'] = datetime.now(tz)
        result = self.mongo.db.users.insert_one(user_data)
        logging.info(f"User created with ID: {result.inserted_id}")
        return result.inserted_id
    
    def get_user_by_google_id(self, google_id):
        """Get user by Google ID."""
        return self.mongo.db.users.find_one({"google_id": google_id})
    
    def get_user_by_email(self, email):
        """Get user by email."""
        return self.mongo.db.users.find_one({"email": email})
    
    def update_user(self, google_id, update_data):
        """Update user information."""
        update_data['updated_at'] = datetime.now(tz)
        result = self.mongo.db.users.update_one(
            {"google_id": google_id}, 
            {"$set": update_data}
        )
        logging.info(f"User updated: {result.modified_count} documents modified")
        return result.modified_count
    
    def delete_user(self, google_id):
        """Delete a user."""
        result = self.mongo.db.users.delete_one({"google_id": google_id})
        logging.info(f"User deleted: {result.deleted_count} documents deleted")
        return result.deleted_count
