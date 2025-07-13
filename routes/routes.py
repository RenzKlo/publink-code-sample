from flask import Blueprint, request, jsonify
import logging
from services.route_service import RouteService
from utils.jwt_service import jwt_required
from utils.decorators import handle_errors

routes_bp = Blueprint('routes', __name__, url_prefix='/api/routes')


@routes_bp.route('/generate', methods=['POST'])
@jwt_required
@handle_errors
def generate_route():
    """Generate a route between origin and destination."""
    logging.info("Route generation started")
    
    # Log raw request data
    raw_data = request.get_data(as_text=True)
    logging.info(f"Raw request data: {raw_data}")
    logging.info(f"Request headers: {dict(request.headers)}")
    logging.info(f"Request content type: {request.content_type}")
    
    data = request.get_json()
    logging.info(f"Parsed JSON data: {data}")
    
    if data is None:
        logging.error("No JSON data received or invalid JSON format")
        return jsonify({"error": "Invalid JSON data"}), 400
    
    origin_data = data.get("origin")
    destination_data = data.get("destination")
    walk_radius = data.get("walk_radius")
    
    logging.info(f"Origin data: {origin_data}")
    logging.info(f"Destination data: {destination_data}")
    logging.info(f"Walk radius: {walk_radius}")
    logging.info(f"User info: {request.user}")

    if not origin_data or not destination_data:
        logging.warning("Origin and Destination are required")
        return jsonify({"error": "Origin and Destination are required"}), 400
    
    # Validate origin and destination structure
    if not isinstance(origin_data, dict) or "lng" not in origin_data or "lat" not in origin_data:
        logging.error(f"Invalid origin format: {origin_data}")
        return jsonify({"error": "Origin must contain 'lng' and 'lat' fields"}), 400
        
    if not isinstance(destination_data, dict) or "lng" not in destination_data or "lat" not in destination_data:
        logging.error(f"Invalid destination format: {destination_data}")
        return jsonify({"error": "Destination must contain 'lng' and 'lat' fields"}), 400
    
    # Parse the data into tuples
    try:
        origin = (float(origin_data["lng"]), float(origin_data["lat"]))
        destination = (float(destination_data["lng"]), float(destination_data["lat"]))
        walk_radius = float(walk_radius) if walk_radius is not None else 100.0
        
        logging.info(f"Parsed origin: {origin}")
        logging.info(f"Parsed destination: {destination}")
        logging.info(f"Parsed walk_radius: {walk_radius}")
        
    except (ValueError, TypeError) as e:
        logging.error(f"Error parsing coordinates: {e}")
        return jsonify({"error": "Invalid coordinate values"}), 400
    
    route_service = RouteService()  # Create instance within route context
    logging.info("RouteService instance created, calling generate_route...")
    
    try:
        route = route_service.generate_route(origin, destination, walk_radius)
        logging.info(f"Route generated successfully: {type(route)} with length {len(route) if hasattr(route, '__len__') else 'N/A'}")
        logging.info(f"Route content: {route}")
        
        # Store the route in user history
        user_id = request.user["sub"]
        logging.info(f"Storing route in history for user: {user_id}")
        route_service.store_route_in_history(user_id, origin, destination, route)
        logging.info("Route stored in history successfully")

        return jsonify(route)
        
    except Exception as e:
        logging.error(f"Error in route generation or storage: {e}")
        return jsonify({"error": "Route generation failed"}), 500


@routes_bp.route('/history', methods=['GET'])
@jwt_required
@handle_errors
def get_user_history():
    """Get user's route request history."""
    user_id = request.user["sub"]
    route_service = RouteService()  # Create instance within route context
    history = route_service.get_user_history(user_id)
    logging.info("Fetched user request history successfully")
    return jsonify(history)


@routes_bp.route('/', methods=['GET'])
@handle_errors
def get_all_routes():
    """Get all available routes."""
    route_service = RouteService()  # Create instance within route context
    route_list = route_service.get_cached_routes()
    logging.info("Fetched all routes successfully")
    return jsonify(route_list)


@routes_bp.route('/<route_name>/description', methods=['GET'])
@handle_errors
def get_route_description(route_name):
    """Get description for a specific route."""
    if not route_name:
        logging.warning("route_name is required")
        return jsonify({"error": "route_name is required"}), 400
    
    route_service = RouteService()  # Create instance within route context
    route = route_service.get_cached_route_description(route_name)
    if not route:
        logging.warning("Route not found")
        return jsonify({"error": "Route not found"}), 404
    
    logging.info("Fetched route description successfully")
    return jsonify(route)


@routes_bp.route('/<route_id>', methods=['GET'])
@handle_errors
def get_route(route_id):
    """Get a specific route by route_id."""
    if not route_id:
        logging.warning("route_id is required")
        return jsonify({"error": "route_id is required"}), 400
    
    route_service = RouteService()  # Create instance within route context
    route = route_service.get_cached_route(route_id)
    if not route:
        logging.warning("Route not found")
        return jsonify({"error": "route not found"}), 404
    
    logging.info("Fetched route successfully")
    return jsonify(route)
