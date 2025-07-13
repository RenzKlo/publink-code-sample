from flask import Blueprint, jsonify
import logging
from services.poi_service import POIService
from utils.decorators import handle_errors

pois_bp = Blueprint('pois', __name__, url_prefix='/api/pois')


@pois_bp.route('/', methods=['GET'])
@handle_errors
def get_pois():
    """Get all Points of Interest."""
    poi_service = POIService()  # Create instance within route context
    pois_list = poi_service.get_cached_pois()
    logging.info("Fetched POIs successfully")
    return jsonify(pois_list)
