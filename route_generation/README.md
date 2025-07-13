# Route Generation Module

This module provides the core route generation system for a public transportation route planning service. It demonstrates intelligent pathfinding between locations using public transportation routes with support for walking connections and multi-modal transfers.

## 🏗️ Architecture Overview

```
route_generation/
├── __init__.py              # Main RouteGenerator class
├── models/
│   ├── __init__.py
│   └── route_models.py      # Data models (RouteResult, RouteSegment, etc.)
├── services/
│   ├── __init__.py
│   ├── graph_service.py     # Graph operations and data loading
│   ├── pathfinding_service.py # A* algorithm implementation
│   └── geojson_service.py   # GeoJSON generation
└── utils/
    ├── __init__.py
    ├── geometry_utils.py    # Geometric calculations
    └── fare_calculator.py   # Fare calculation logic
```

## 🚀 Features

### **Route Planning**
- **Multi-modal routing**: Combines walking and public transportation
- **Optimal pathfinding**: Uses efficient algorithms for route discovery
- **Transfer optimization**: Minimizes transfers between different routes
- **Walking distance control**: Configurable maximum walking distances

### **Data Models**
- **Structured data**: Well-defined models for routes, coordinates, and segments
- **Type safety**: Comprehensive type hints for better code reliability
- **Validation**: Input validation and error handling

### **GeoJSON Output**
- **Standard format**: Generates GeoJSON for map visualization
- **Route visualization**: Includes route colors, fare information, and distances
- **Summary data**: Provides totals for distance, fare, and transfers

### **Performance**
- **Graph optimization**: Efficient graph pruning and caching
- **Memory management**: Optimized for handling large route networks
- **Logging**: Comprehensive logging for monitoring and debugging

## 📖 Usage Examples

### Basic Route Generation
```python
from route_gen_clean import route_generator

# Generate routes between two coordinates
start_coord = (122.5734, 10.6924)  # longitude, latitude
end_coord = (122.5752, 10.7032)
walk_radius = 100  # meters

routes = route_generator(start_coord, end_coord, walk_radius)
```

### Using the RouteGenerator Class
```python
from route_generation import RouteGenerator

# Create generator instance
generator = RouteGenerator()

# Generate routes with custom walking radius
routes = generator.generate_route(start_coord, end_coord, walk_radius)

# Process the results
for route in routes:
    features = route['features']
    for feature in features:
        if feature['geometry'] is None:  # Summary feature
            props = feature['properties']
            print(f"Distance: {props['total_distance']}km")
            print(f"Fare: ₱{props['total_fare']}")
            print(f"Transfers: {props['total_transfers']}")
```

### Working with Route Data
```python
from route_generation.models.route_models import Coordinate, RouteSegment

# Create coordinate objects
start = Coordinate(longitude=122.5734, latitude=10.6924)
end = Coordinate(longitude=122.5752, latitude=10.7032)

# Work with route segments
segment = RouteSegment(
    route_name="Route 1",
    start_coordinate=start,
    end_coordinate=end,
    distance_km=2.5,
    fare=12.0,
    coordinates=[start, end]
)

# Convert to dictionary for JSON serialization
segment_dict = segment.to_dict()
```

## ⚙️ Configuration

### Data Sources
The module loads route data from MongoDB and supports custom data loading:

```python
# Configure MongoDB connection in GraphService
class GraphService:
    def load_main_graph(self):
        # Load transportation route network from MongoDB
        # Returns NetworkX graph with route connections
        pass
        
    def load_positions(self):
        # Load coordinate positions for route nodes
        pass
        
    def load_routes(self):
        # Load route definitions and metadata
        pass
```

### Fare Calculation
Configure fare calculation parameters:

```python
from route_generation.utils.fare_calculator import FareCalculator

calculator = FareCalculator()
calculator.min_fare_regular = 12.0          # Minimum fare
calculator.min_fare_kilometers = 4.0        # Distance for minimum fare
calculator.fare_per_km_regular = 1.8        # Additional fare per km
```

## 🧪 Testing

### Unit Testing
Test individual components of the route generation system:

```python
import unittest
from route_generation.utils.geometry_utils import GeometryUtils

class TestGeometryUtils(unittest.TestCase):
    def setUp(self):
        self.geo_utils = GeometryUtils()
    
    def test_haversine_distance(self):
        coord1 = (122.5734, 10.6924)
        coord2 = (122.5752, 10.7032)
        distance = self.geo_utils.haversine_distance(coord1, coord2)
        self.assertGreater(distance, 0)
```

### Integration Testing
Test the complete route generation workflow:

```python
from route_generation import RouteGenerator

def test_route_generation():
    generator = RouteGenerator()
    routes = generator.generate_route(
        (122.5734, 10.6924),
        (122.5752, 10.7032),
        100
    )
    assert len(routes) > 0
    assert routes[0]['type'] == 'FeatureCollection'
```

## 📊 Monitoring and Logging

### Logging Configuration
The module provides comprehensive logging for monitoring route generation:

```python
import logging

# Configure logging to see route generation details
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# The system logs:
# - Route generation performance
# - Graph loading statistics
# - Pathfinding progress
# - Error conditions and debugging info
```

### Performance Metrics
Access graph and routing statistics:

```python
from route_generation import RouteGenerator

generator = RouteGenerator()

# Get information about the loaded route network
graph_stats = generator.graph_service.get_graph_statistics(graph)
print(f"Route nodes: {graph_stats['nodes']}")
print(f"Route connections: {graph_stats['edges']}")
print(f"Network density: {graph_stats['density']}")
```

## 🔄 Integration

### Flask API Integration
The route generation module integrates with the Flask API:

```python
# In your Flask route handler
from route_generation import RouteGenerator

@app.route('/api/routes/generate', methods=['POST'])
def generate_route():
    data = request.get_json()
    
    generator = RouteGenerator()
    routes = generator.generate_route(
        origin=data['origin'],
        destination=data['destination'], 
        walk_radius=data.get('walk_radius', 100)
    )
    
    return jsonify(routes)
```

## 🐛 Troubleshooting

### Common Issues

**1. Import Errors**
```python
# Make sure the route_generation directory is in your Python path
import sys
sys.path.append('/path/to/your/server/directory')
```

**2. Missing Dependencies**
```bash
pip install networkx shapely pymongo
```

**3. Graph Data Not Loading**
- Implement the data loading methods in `GraphService`
- Check your MongoDB connection
- Verify data format compatibility

**4. Performance Issues**
- Check graph pruning parameters
- Monitor memory usage during large route calculations
- Consider caching frequently used routes

## 🚀 System Capabilities

### Current Features
- ✅ Multi-modal route planning (walking + public transit)
- ✅ Advanced pathfinding algorithms
- ✅ GeoJSON output format
- ✅ Fare calculation
- ✅ Transfer optimization
- ✅ MongoDB integration
- ✅ Comprehensive logging
- ✅ Type-safe code structure

### Route Planning Algorithm
The system uses advanced pathfinding algorithms to find optimal routes by:
1. Loading transportation route network from MongoDB
2. Creating a graph representation of routes and connections
3. Finding nearby route access points within walking distance
4. Computing optimal paths considering distance, transfers, and fare
5. Generating GeoJSON output for map visualization

## 📚 API Reference

### Core Classes

#### `RouteGenerator`
Main class for route generation operations.

**Methods:**
- `generate_route(start_coord, end_coord, radius)` - Generate optimal routes
- `_prepare_graph(start_coord, end_coord)` - Prepare graph with start/end nodes
- `_find_nearby_edges(coordinate, radius)` - Find edges within radius
- `_select_best_routes(iterations)` - Select optimal routes from computed paths

#### `RouteResult`
Complete route result with all segments.

**Properties:**
- `segments: List[RouteSegment]` - Individual route segments
- `total_distance_km: float` - Total distance in kilometers
- `total_fare: float` - Total fare in currency units
- `total_transfers: int` - Number of required transfers

#### `GeometryUtils`
Utility class for geometric calculations.

**Methods:**
- `haversine_distance(coord1, coord2)` - Calculate distance between coordinates
- `nearest_edges_within_radius(routes, positions, coordinate, radius)` - Find nearby edges

---

**Transportation Route Generation System** - Intelligent route planning for public transportation systems.
