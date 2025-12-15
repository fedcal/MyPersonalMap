"""
Geographic Utilities Service

Provides geographic calculations without requiring spatial database extensions.
Uses pure Python with math formulas (Haversine) for distance calculations.
"""

import math
from typing import Tuple


# Earth's radius in different units
EARTH_RADIUS_KM = 6371.0
EARTH_RADIUS_MILES = 3959.0
EARTH_RADIUS_METERS = 6371000.0


def validate_coordinates(latitude: float, longitude: float) -> bool:
    """
    Validate geographic coordinates

    Args:
        latitude: Latitude in decimal degrees
        longitude: Longitude in decimal degrees

    Returns:
        True if coordinates are valid, False otherwise

    Example:
        >>> validate_coordinates(45.4642, 9.1900)
        True
        >>> validate_coordinates(91.0, 0.0)
        False
    """
    return -90.0 <= latitude <= 90.0 and -180.0 <= longitude <= 180.0


def haversine_distance(
    lat1: float,
    lon1: float,
    lat2: float,
    lon2: float,
    unit: str = 'km'
) -> float:
    """
    Calculate distance between two points using Haversine formula

    The Haversine formula calculates the great-circle distance between two points
    on a sphere given their longitudes and latitudes. This is accurate for most
    use cases (error < 0.5%).

    Args:
        lat1: Latitude of first point in decimal degrees
        lon1: Longitude of first point in decimal degrees
        lat2: Latitude of second point in decimal degrees
        lon2: Longitude of second point in decimal degrees
        unit: Unit of distance ('km', 'miles', 'meters')

    Returns:
        Distance in specified unit

    Raises:
        ValueError: If coordinates are invalid or unit is unsupported

    Example:
        >>> # Distance from Milan to Rome
        >>> haversine_distance(45.4642, 9.1900, 41.9028, 12.4964)
        477.58
    """
    # Validate coordinates
    if not (validate_coordinates(lat1, lon1) and validate_coordinates(lat2, lon2)):
        raise ValueError("Invalid coordinates")

    # Select earth radius based on unit
    if unit == 'km':
        radius = EARTH_RADIUS_KM
    elif unit == 'miles':
        radius = EARTH_RADIUS_MILES
    elif unit == 'meters':
        radius = EARTH_RADIUS_METERS
    else:
        raise ValueError(f"Unsupported unit: {unit}. Use 'km', 'miles', or 'meters'")

    # Convert to radians
    lat1_rad = math.radians(lat1)
    lon1_rad = math.radians(lon1)
    lat2_rad = math.radians(lat2)
    lon2_rad = math.radians(lon2)

    # Haversine formula
    dlat = lat2_rad - lat1_rad
    dlon = lon2_rad - lon1_rad

    a = (
        math.sin(dlat / 2) ** 2 +
        math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon / 2) ** 2
    )
    c = 2 * math.asin(math.sqrt(a))

    return radius * c


def get_bounding_box(
    latitude: float,
    longitude: float,
    distance_km: float
) -> Tuple[float, float, float, float]:
    """
    Calculate bounding box for a given point and distance

    Returns a bounding box (min_lat, min_lon, max_lat, max_lon) that encompasses
    all points within the specified distance from the center point.

    Args:
        latitude: Center point latitude
        longitude: Center point longitude
        distance_km: Radius in kilometers

    Returns:
        Tuple of (min_lat, min_lon, max_lat, max_lon)

    Example:
        >>> # Bounding box within 10km of Milan center
        >>> get_bounding_box(45.4642, 9.1900, 10)
        (45.3742, 9.0567, 45.5542, 9.3233)
    """
    if not validate_coordinates(latitude, longitude):
        raise ValueError("Invalid coordinates")

    # Approximate degrees per km (varies by latitude)
    # At equator: 1 degree ≈ 111 km
    # Adjust for latitude
    lat_degree_km = 111.0
    lon_degree_km = 111.0 * math.cos(math.radians(latitude))

    lat_delta = distance_km / lat_degree_km
    lon_delta = distance_km / lon_degree_km

    min_lat = max(latitude - lat_delta, -90.0)
    max_lat = min(latitude + lat_delta, 90.0)
    min_lon = max(longitude - lon_delta, -180.0)
    max_lon = min(longitude + lon_delta, 180.0)

    return (min_lat, min_lon, max_lat, max_lon)


def is_point_in_bounding_box(
    point_lat: float,
    point_lon: float,
    bbox: Tuple[float, float, float, float]
) -> bool:
    """
    Check if a point is within a bounding box

    Args:
        point_lat: Point latitude
        point_lon: Point longitude
        bbox: Bounding box (min_lat, min_lon, max_lat, max_lon)

    Returns:
        True if point is within bounding box

    Example:
        >>> bbox = get_bounding_box(45.4642, 9.1900, 10)
        >>> is_point_in_bounding_box(45.5, 9.2, bbox)
        True
    """
    min_lat, min_lon, max_lat, max_lon = bbox
    return (
        min_lat <= point_lat <= max_lat and
        min_lon <= point_lon <= max_lon
    )


def bearing(
    lat1: float,
    lon1: float,
    lat2: float,
    lon2: float
) -> float:
    """
    Calculate initial bearing from point 1 to point 2

    Args:
        lat1: Latitude of first point
        lon1: Longitude of first point
        lat2: Latitude of second point
        lon2: Longitude of second point

    Returns:
        Bearing in degrees (0-360, where 0/360 is North, 90 is East)

    Example:
        >>> # Bearing from Milan to Rome
        >>> bearing(45.4642, 9.1900, 41.9028, 12.4964)
        160.5  # Approximately SE
    """
    if not (validate_coordinates(lat1, lon1) and validate_coordinates(lat2, lon2)):
        raise ValueError("Invalid coordinates")

    lat1_rad = math.radians(lat1)
    lat2_rad = math.radians(lat2)
    dlon_rad = math.radians(lon2 - lon1)

    y = math.sin(dlon_rad) * math.cos(lat2_rad)
    x = (
        math.cos(lat1_rad) * math.sin(lat2_rad) -
        math.sin(lat1_rad) * math.cos(lat2_rad) * math.cos(dlon_rad)
    )

    bearing_rad = math.atan2(y, x)
    bearing_deg = math.degrees(bearing_rad)

    # Normalize to 0-360
    return (bearing_deg + 360) % 360


def midpoint(
    lat1: float,
    lon1: float,
    lat2: float,
    lon2: float
) -> Tuple[float, float]:
    """
    Calculate midpoint between two coordinates

    Args:
        lat1: Latitude of first point
        lon1: Longitude of first point
        lat2: Latitude of second point
        lon2: Longitude of second point

    Returns:
        Tuple of (midpoint_lat, midpoint_lon)

    Example:
        >>> # Midpoint between Milan and Rome
        >>> midpoint(45.4642, 9.1900, 41.9028, 12.4964)
        (43.69, 10.84)
    """
    if not (validate_coordinates(lat1, lon1) and validate_coordinates(lat2, lon2)):
        raise ValueError("Invalid coordinates")

    lat1_rad = math.radians(lat1)
    lon1_rad = math.radians(lon1)
    lat2_rad = math.radians(lat2)
    dlon_rad = math.radians(lon2 - lon1)

    bx = math.cos(lat2_rad) * math.cos(dlon_rad)
    by = math.cos(lat2_rad) * math.sin(dlon_rad)

    mid_lat_rad = math.atan2(
        math.sin(lat1_rad) + math.sin(lat2_rad),
        math.sqrt((math.cos(lat1_rad) + bx) ** 2 + by ** 2)
    )
    mid_lon_rad = lon1_rad + math.atan2(by, math.cos(lat1_rad) + bx)

    return (math.degrees(mid_lat_rad), math.degrees(mid_lon_rad))
