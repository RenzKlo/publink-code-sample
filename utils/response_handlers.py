from flask import request
import logging


def after_request(response):
    """Handle response modifications after each request."""
    response.direct_passthrough = False
    response_size = len(response.get_data())
    logging.info(f"Response size: {response_size} bytes")
    response.headers["Content-Length"] = response_size
    response.headers["Connection"] = "keep-alive"
    
    # Add CORS headers if needed
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
    
    return response
