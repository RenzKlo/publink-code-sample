"""
Route Models Module

Data models for route generation system.
"""

from typing import List, Tuple, Optional, Dict, Any
from dataclasses import dataclass


@dataclass
class Coordinate:
    """Represents a geographic coordinate."""
    longitude: float
    latitude: float
    
    def to_tuple(self) -> Tuple[float, float]:
        """Convert to (longitude, latitude) tuple."""
        return (self.longitude, self.latitude)
    
    @classmethod
    def from_tuple(cls, coord: Tuple[float, float]) -> 'Coordinate':
        """Create from (longitude, latitude) tuple."""
        return cls(longitude=coord[0], latitude=coord[1])


@dataclass
class RouteSegment:
    """Represents a segment of a route."""
    route_name: str
    start_coordinate: Coordinate
    end_coordinate: Coordinate
    distance_km: float
    fare: float
    coordinates: List[Coordinate]
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary representation."""
        return {
            'route': self.route_name,
            'start_coordinate': self.start_coordinate.to_tuple(),
            'end_coordinate': self.end_coordinate.to_tuple(),
            'distance': round(self.distance_km, 2),
            'fare': round(self.fare, 2),
            'coordinates': [coord.to_tuple() for coord in self.coordinates]
        }


@dataclass
class RouteResult:
    """Complete route result with all segments."""
    segments: List[RouteSegment]
    total_distance_km: float
    total_fare: float
    total_transfers: int
    walk_distance_km: float
    iteration: int
    
    def to_geojson(self) -> Dict[str, Any]:
        """Convert to GeoJSON format."""
        features = []
        
        # Add total summary feature
        total_feature = {
            "type": "Feature",
            "geometry": None,
            "properties": {
                "iteration": self.iteration,
                "total_distance": round(self.total_distance_km, 2),
                "total_fare": round(self.total_fare, 2),
                "shortest_walk_distance": round(self.walk_distance_km, 2),
                "total_transfers": self.total_transfers,
            }
        }
        features.append(total_feature)
        
        # Add segment features
        for segment in self.segments:
            if segment.coordinates and len(segment.coordinates) >= 2:
                segment_feature = {
                    "type": "Feature",
                    "properties": {
                        "route": segment.route_name,
                        "route_distance": round(segment.distance_km, 2),
                        "route_fare": round(segment.fare, 2),
                        "color": self._get_route_color(segment.route_name)
                    },
                    "geometry": {
                        "type": "LineString",
                        "coordinates": [coord.to_tuple() for coord in segment.coordinates]
                    },
                }
                features.append(segment_feature)
        
        return {
            "type": "FeatureCollection",
            "features": features
        }
    
    def _get_route_color(self, route_name: str) -> str:
        """Get color for route visualization."""
        route_colors = {
            "Route 1": "#226C0A",
            "Route 2": "#FB121A",
            "Route 3": "#08056E",
            "Route 4": "#4E0881",
            "Route 5": "#A5AD0B",
            "Route 6": "#387AED",
            "Route 7": "#13409F",
            "Route 8": "#43A755",
            "Route 9": "#FD4217",
            "Route 10": "#D56844",
            "Route 11": "#323230",
            "Route 12": "#5BAE40",
            "Route 13": "#66A5CD",
            "Route 14": "#5A3408",
            "Route 15": "#FBC12D",
            "Route 16": "#040232",
            "Route 17": "#092308",
            "Route 18": "#A75214",
            "Route 19": "#A90F84",
            "Route 20": "#72C5C3",
            "Route 21": "#C57216",
            "Route 22": "#7CBD74",
            "Route 23": "#19A5C5",
            "Route 24": "#B95E32",
            "Route 25": "#F7A51E",
            "Route 26": "#2C3E50",
            "Route 27": "#E74C3C",
            "Route 28": "#F1C40F",
            "Route 29": "#2ECC71",
            "Route 30": "#3498DB",
            "Route 31": "#9B59B6",
            "Route 32": "#E67E22",
            "Transfer": "#808080"
        }
        return route_colors.get(route_name, "#000000")


@dataclass
class EdgeInfo:
    """Information about a graph edge."""
    start_node: str
    end_node: str
    route_name: str
    weight: float
    coordinates: List[Coordinate]


@dataclass
class SearchResult:
    """Result of pathfinding search."""
    path: Optional[List[Tuple]]
    visited_nodes: int
    checked_nodes: int
    success: bool
    error_message: Optional[str] = None


@dataclass
class RouteOptions:
    """Configuration options for route generation."""
    max_walking_distance: float = 0.5  # km
    max_transfers: int = 3
    prefer_distance: bool = False
    prefer_fare: bool = True
    include_walking: bool = True
    penalty_per_transfer: float = 0.01  # 1% penalty per transfer


@dataclass
class NearbyEdge:
    """Information about a nearby edge."""
    edge: Tuple[str, str]
    route_name: str
    nearest_point: Coordinate
    distance_meters: float
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary representation."""
        return {
            'edge': self.edge,
            'route_name': self.route_name,
            'nearest_point': self.nearest_point.to_tuple(),
            'distance_meters': round(self.distance_meters, 2)
        }
