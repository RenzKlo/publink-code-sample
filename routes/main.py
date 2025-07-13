from flask import Blueprint, jsonify
import logging

main_bp = Blueprint('main', __name__)


@main_bp.route('/')
def home():
    """Main home route."""
    logging.info("Home route accessed")
    return jsonify({"message": "PubLink API - Connected", "status": "online"}), 200


@main_bp.route('/health')
def health_check():
    """Health check endpoint."""
    return jsonify({"status": "healthy", "service": "publink-api"}), 200


@main_bp.route('/db-test')
def database_test():
    """Test database connection."""
    try:
        from flask import current_app
        
        # Test MongoDB connection
        mongo = current_app.extensions['pymongo']
        
        # Try to ping the database
        db_info = mongo.db.command("ping")
        
        # Get database stats
        stats = mongo.db.command("dbStats")
        
        # Count collections
        collections = mongo.db.list_collection_names()
        
        # Test a simple query (count users)
        user_count = mongo.db.users.count_documents({})
        
        return jsonify({
            "status": "success",
            "database": "connected",
            "ping": db_info,
            "database_name": stats.get("db", "unknown"),
            "collections": collections,
            "collections_count": len(collections),
            "users_count": user_count,
            "connection_string_host": mongo.cx.address if hasattr(mongo.cx, 'address') else "Atlas Cluster"
        }), 200
        
    except Exception as e:
        logging.error(f"Database connection test failed: {str(e)}")
        return jsonify({
            "status": "error",
            "database": "disconnected",
            "error": str(e),
            "error_type": type(e).__name__
        }), 500


@main_bp.route('/debug-routes')
def debug_routes():
    """Debug jeepney_routes collection structure."""
    try:
        from flask import current_app
        
        # Test MongoDB connection
        mongo = current_app.extensions['pymongo']
        
        # Get sample documents from jeepney_routes collection
        routes_collection = mongo.db.jeepney_routes
        total_routes = routes_collection.count_documents({})
        
        # Get a few sample documents
        samples = list(routes_collection.find({}).limit(3))
        
        # Analyze the structure
        analysis = {
            "total_routes": total_routes,
            "sample_count": len(samples),
            "document_structures": []
        }
        
        for i, sample in enumerate(samples):
            doc_analysis = {
                "document_index": i,
                "keys": list(sample.keys()) if sample else [],
                "sample_data": {}
            }
            
            if sample:
                # Check for coordinate-related fields
                coord_fields = ['coordinates', 'coords', 'geometry', 'route', 'path', 'points', 'features']
                for field in coord_fields:
                    if field in sample:
                        value = sample[field]
                        doc_analysis["sample_data"][field] = {
                            "type": str(type(value).__name__),
                            "length": len(value) if hasattr(value, '__len__') else "N/A",
                            "sample": str(value)[:200] + "..." if len(str(value)) > 200 else str(value)
                        }
                
                # Add other important fields
                for key in ['name', 'uid', 'id', 'route_name']:
                    if key in sample:
                        doc_analysis["sample_data"][key] = str(sample[key])
            
            analysis["document_structures"].append(doc_analysis)
        
        return jsonify(analysis), 200
        
    except Exception as e:
        logging.error(f"Error in debug-routes: {e}")
        return jsonify({"error": str(e)}), 500
