#!/usr/bin/env python3
"""
Development server runner with hot reload and debugging.
Use this for local development only.
"""

import os
import logging
from app_new import create_app
from flask.cli import with_appcontext
import click

# Load environment variables from .env file
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    print("Warning: python-dotenv not installed. Consider installing it for .env support")

# Create app with development config
app = create_app('development')

@app.cli.command()
def init_db():
    """Initialize the database."""
    click.echo('Initializing the database...')
    # Add database initialization logic here
    click.echo('Database initialized.')

@app.cli.command()
def test():
    """Run the tests."""
    import subprocess
    try:
        subprocess.run(['pytest', '-v', 'tests/'], check=True)
    except FileNotFoundError:
        click.echo("pytest not found. Install with: pip install pytest")
    except subprocess.CalledProcessError:
        click.echo("Some tests failed.")

if __name__ == '__main__':
    # Configure logging for development
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s %(levelname)s [%(name)s]: %(message)s"
    )
    
    # Get configuration from environment
    host = os.getenv('FLASK_HOST', '127.0.0.1')
    port = int(os.getenv('FLASK_PORT', 5000))
    
    print("🚀 Starting PubLink Development Server")
    print(f"📍 Running on http://{host}:{port}")
    print("🔄 Auto-reload enabled")
    print("🐛 Debug mode enabled")
    print("⏹️  Press Ctrl+C to stop")
    
    # Run development server
    app.run(
        host=host,
        port=port,
        debug=True,
        threaded=True,
        use_reloader=True
    )
