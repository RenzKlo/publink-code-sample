import logging
from datetime import datetime
import pytz
from flask import current_app
from config import Config
from route_gen_clean import route_generator

tz = pytz.timezone(Config.TIMEZONE)


class RouteService:
    """Service class for handling route-related operations."""
    
    def __init__(self):
        # Get the database connection from the current Flask app context
        if current_app:
            self.mongo = current_app.extensions['pymongo']
        else:
            self.mongo = None
    
    def generate_route(self, origin, destination, walk_radius):
        """Generate a route between origin and destination."""
        return route_generator(origin, destination, walk_radius)
    
    def store_route_in_history(self, user_id, origin, destination, route):
        """Store route in user's history."""
        if not self.mongo:
            raise RuntimeError("Database connection not available")
            
        self.mongo.db.user_history.insert_one({
            "user_id": user_id,
            "origin": origin,
            "destination": destination,
            "route": route,
            "timestamp": datetime.now(tz),
        })
        logging.info("Route stored in user history")
    
    def get_user_history(self, user_id):
        """Get user's route history."""
        if not self.mongo:
            raise RuntimeError("Database connection not available")
            
        history = self.mongo.db.user_history.find(
            {"user_id": user_id}, 
            {"_id": 0}
        ).sort("timestamp", -1)
        return list(history)
    
    def get_cached_routes(self):
        """Get all cached routes."""
        if not self.mongo:
            raise RuntimeError("Database connection not available")
            
        collection = self.mongo.db.route_descriptions
        routes = collection.find(
            {}, 
            {"_id": 0, "route_id": 1, "route_name": 1, "route_desc": 1}
        )
        return list(routes)
    
    def get_cached_route_description(self, route_id):
        """Get route description by route ID."""
        if not self.mongo:
            raise RuntimeError("Database connection not available")
            
        collection = self.mongo.db.route_description
        return collection.find_one(
            {"route_id": route_id}, 
            {"_id": 0, "jeepney_route_id": 0}
        )
    
    def get_cached_route(self, route_name):
        """Get route by route name."""
        if not self.mongo:
            raise RuntimeError("Database connection not available")
            
        collection = self.mongo.db.jeepney_routes
        return collection.find_one(
            {"name": route_name}, 
            {"_id": 0, "name": 0, "uid": 0}
        )
