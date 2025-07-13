# Publink API Server

A Flask-based REST API for a public transportation routing system. This project demonstrates backend development skills including API design, authentication, database integration, and microservices architecture.
*This project serves as a comprehensive example of modern Python backend development, demonstrating scalable architecture, security best practices, and production-ready deployment strategies.*

## Project Structure

```
src/server/
├── app_new.py              # Application entry point
├── run_dev.py              # Development server runner
├── config.py               # Configuration classes
├── requirements.txt        # Python dependencies
├── Dockerfile             # Docker configuration
├── docker-compose.yml     # Docker Compose for development
├── .env.example           # Environment variables template
├── models/                # Data models
├── routes/                # Blueprint route handlers
│   ├── __init__.py
│   ├── main.py           # Main routes
│   ├── auth.py           # Authentication routes
│   ├── routes.py         # Route generation endpoints
│   └── pois.py           # Points of Interest endpoints
├── services/              # Business logic layer
│   ├── __init__.py
│   ├── route_service.py  # Route-related operations
│   ├── poi_service.py    # POI-related operations
│   └── user_service.py   # User-related operations
├── utils/                 # Utility modules
│   ├── __init__.py
│   ├── auth.py           # Authentication utilities
│   ├── decorators.py     # Common decorators
│   ├── error_handlers.py # Error handling
│   └── response_handlers.py # Response processing
└── route_generation/      # Route generation algorithms

```

*More details of the route_generation module can b found on its own README file.*

## Features

- **Application Factory Pattern**: Clean, testable application structure
- **Blueprint Architecture**: Organized route handling
- **Service Layer**: Separation of business logic
- **Configuration Management**: Environment-specific settings
- **Authentication**: Google OAuth integration
- **Error Handling**: Comprehensive error management
- **Logging**: Structured logging throughout the application
- **Docker Support**: Containerized deployment
- **MongoDB Integration**: Document-based data storage

## Technical Stack

- **Backend Framework**: Flask with Blueprint architecture
- **Database**: MongoDB with PyMongo driver
- **Authentication**: Google OAuth 2.0 + JWT
- **Containerization**: Docker & Docker Compose
- **Process Management**: Gunicorn WSGI server
- **Development Tools**: Environment configuration, logging, error handling

## Installation

### Local Development

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd transportation-api/src/server
   ```

2. **Create virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**:
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

5. **Run the development server**:
   ```bash
   python run_dev.py
   ```

### Docker Development

1. **Using Docker Compose** (includes MongoDB):
   ```bash
   docker-compose up --build
   ```

2. **Using Docker only**:
   ```bash
   docker build -t transportation-server .
   docker run -p 5000:5000 -e MONGO_URI=<your-mongo-uri> transportation-server
   ```

## Configuration

The application uses different configuration classes for different environments:

- `DevelopmentConfig`: Local development settings
- `ProductionConfig`: Production deployment settings
- `TestingConfig`: Testing environment settings

Set the `FLASK_ENV` environment variable to switch between configurations:
- `development` (default)
- `production`
- `testing`

## API Endpoints

### Authentication
- `POST /auth/google` - Google OAuth authentication

### Routes
- `POST /api/routes/generate` - Generate route between two points
- `GET /api/routes/history` - Get user's route history
- `GET /api/routes/` - Get all available routes
- `GET /api/routes/<route_name>/description` - Get route description
- `GET /api/routes/<route_id>` - Get specific route details

### Points of Interest
- `GET /api/get_pois` - Get all POIs

### Main
- `GET /` - Health check
- `GET /health` - Service health status

## Environment Variables

Create a `.env` file based on `.env.example`:

```env
FLASK_ENV=development
FLASK_HOST=0.0.0.0
FLASK_PORT=5000
SECRET_KEY=your-secret-key-here
MONGO_URI=mongodb://localhost:27017/transportation_db
GOOGLE_CLIENT_ID=your-google-client-id-here
LOG_LEVEL=DEBUG
```

## Development

### Adding New Routes

1. Create a new blueprint in `routes/`
2. Register the blueprint in `__init__.py`
3. Add business logic to appropriate service in `services/`

### Adding New Services

1. Create service class in `services/`
2. Import and use in route handlers
3. Add any required models in `models/`

### Testing

```bash
# Set testing environment
export FLASK_ENV=testing

# Run tests (when test suite is added)
python -m pytest
```

## Deployment

### Production Deployment

1. **Set environment variables**:
   ```bash
   export FLASK_ENV=production
   export SECRET_KEY=<secure-secret-key>
   export MONGO_URI=<production-mongo-uri>
   export GOOGLE_CLIENT_ID=<production-client-id>
   ```

2. **Using Gunicorn**:
   ```bash
   gunicorn --bind 0.0.0.0:5000 --workers 4 app_new:app
   ```

3. **Using Docker**:
   ```bash
   docker build -t transportation-server .
   docker run -d -p 5000:5000 \
     -e FLASK_ENV=production \
     -e SECRET_KEY=<secret> \
     -e MONGO_URI=<uri> \
     transportation-server
   ```

## Backend Architecture & Skills Demonstrated

This project showcases several backend development best practices and skills:

### **System Design**
- **Microservices Architecture**: Modular service-oriented design
- **Separation of Concerns**: Clear separation between routes, services, and utilities
- **Application Factory Pattern**: Scalable Flask application structure
- **Blueprint Organization**: RESTful API endpoint organization

### **Database Integration**
- **MongoDB Integration**: NoSQL document database operations
- **Data Modeling**: Structured data models for transportation systems
- **Query Optimization**: Efficient database queries and indexing

### **Authentication & Security**
- **OAuth Integration**: Google OAuth 2.0 implementation
- **JWT Tokens**: Secure token-based authentication
- **Middleware**: Custom authentication decorators and middleware

### **API Development**
- **RESTful Design**: Well-structured REST API endpoints
- **Error Handling**: Comprehensive error management and HTTP status codes
- **Request Validation**: Input validation and sanitization
- **Response Formatting**: Consistent API response structures

### **DevOps & Deployment**
- **Containerization**: Docker configuration for consistent deployment
- **Environment Management**: Configuration for different deployment stages
- **Logging**: Structured logging for monitoring and debugging
- **Production Ready**: Gunicorn WSGI server configuration



---


