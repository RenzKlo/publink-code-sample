import logging
from flask import current_app


class POIService:
    """Service class for handling Points of Interest operations."""
    
    def __init__(self):
        self.mongo = None  # Will use current_app.extensions['pymongo'] when needed
    
    def get_cached_pois(self):
        """Get all cached Points of Interest."""
        mongo = current_app.extensions['pymongo']
        pois = mongo.db.iloilo_pois.find({}, {"_id": 0})
        return list(pois)
    
    def add_poi(self, poi_data):
        """Add a new Point of Interest."""
        mongo = current_app.extensions['pymongo']
        result = mongo.db.iloilo_pois.insert_one(poi_data)
        logging.info(f"POI added with ID: {result.inserted_id}")
        return result.inserted_id
    
    def update_poi(self, poi_id, update_data):
        """Update an existing Point of Interest."""
        mongo = current_app.extensions['pymongo']
        result = mongo.db.iloilo_pois.update_one(
            {"_id": poi_id}, 
            {"$set": update_data}
        )
        logging.info(f"POI updated: {result.modified_count} documents modified")
        return result.modified_count
    
    def delete_poi(self, poi_id):
        """Delete a Point of Interest."""
        mongo = current_app.extensions['pymongo']
        result = mongo.db.iloilo_pois.delete_one({"_id": poi_id})
        logging.info(f"POI deleted: {result.deleted_count} documents deleted")
        return result.deleted_count
