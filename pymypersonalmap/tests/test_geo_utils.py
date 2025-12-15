"""
Tests for Geographic Utilities Service

Tests for geo_utils.py functions including distance calculations,
bounding boxes, and coordinate validation.
"""

import pytest
import math
from pymypersonalmap.services.geo_utils import (
    validate_coordinates,
    haversine_distance,
    get_bounding_box,
    is_point_in_bounding_box,
    bearing,
    midpoint
)


class TestCoordinateValidation:
    """Tests for coordinate validation"""

    def test_valid_coordinates(self):
        """Test valid coordinate ranges"""
        assert validate_coordinates(0, 0) is True
        assert validate_coordinates(45.4642, 9.1900) is True  # Milan
        assert validate_coordinates(-33.8688, 151.2093) is True  # Sydney
        assert validate_coordinates(90, 180) is True  # Extreme valid
        assert validate_coordinates(-90, -180) is True  # Extreme valid

    def test_invalid_latitude(self):
        """Test invalid latitude values"""
        assert validate_coordinates(91, 0) is False
        assert validate_coordinates(-91, 0) is False
        assert validate_coordinates(100, 0) is False

    def test_invalid_longitude(self):
        """Test invalid longitude values"""
        assert validate_coordinates(0, 181) is False
        assert validate_coordinates(0, -181) is False
        assert validate_coordinates(0, 200) is False

    def test_edge_cases(self):
        """Test edge case coordinates"""
        assert validate_coordinates(90.0, 0) is True
        assert validate_coordinates(-90.0, 0) is True
        assert validate_coordinates(0, 180.0) is True
        assert validate_coordinates(0, -180.0) is True


class TestHaversineDistance:
    """Tests for Haversine distance calculation"""

    def test_same_point(self):
        """Test distance from a point to itself"""
        distance = haversine_distance(45.4642, 9.1900, 45.4642, 9.1900)
        assert distance == 0.0

    def test_milan_to_rome(self):
        """Test distance between Milan and Rome"""
        # Milan: 45.4642, 9.1900
        # Rome: 41.9028, 12.4964
        distance = haversine_distance(45.4642, 9.1900, 41.9028, 12.4964)
        # Expected: ~477 km
        assert 475 < distance < 480

    def test_different_units(self):
        """Test distance in different units"""
        lat1, lon1 = 45.4642, 9.1900  # Milan
        lat2, lon2 = 41.9028, 12.4964  # Rome

        dist_km = haversine_distance(lat1, lon1, lat2, lon2, unit='km')
        dist_miles = haversine_distance(lat1, lon1, lat2, lon2, unit='miles')
        dist_meters = haversine_distance(lat1, lon1, lat2, lon2, unit='meters')

        # Check conversions
        assert abs(dist_km * 0.621371 - dist_miles) < 0.1  # km to miles
        assert abs(dist_km * 1000 - dist_meters) < 100  # km to meters

    def test_invalid_coordinates(self):
        """Test with invalid coordinates"""
        with pytest.raises(ValueError):
            haversine_distance(91, 0, 0, 0)

        with pytest.raises(ValueError):
            haversine_distance(0, 181, 0, 0)

    def test_invalid_unit(self):
        """Test with invalid unit"""
        with pytest.raises(ValueError):
            haversine_distance(0, 0, 1, 1, unit='invalid')

    def test_equator_distance(self):
        """Test distance along equator"""
        # 1 degree of longitude at equator ≈ 111 km
        distance = haversine_distance(0, 0, 0, 1)
        assert 110 < distance < 112

    def test_antipodal_points(self):
        """Test maximum distance (opposite sides of Earth)"""
        # Distance should be approximately half Earth's circumference
        distance = haversine_distance(0, 0, 0, 180)
        expected = math.pi * 6371  # ~20015 km
        assert abs(distance - expected) < 100


class TestBoundingBox:
    """Tests for bounding box calculations"""

    def test_basic_bounding_box(self):
        """Test basic bounding box creation"""
        lat, lon = 45.4642, 9.1900  # Milan
        distance_km = 10

        bbox = get_bounding_box(lat, lon, distance_km)
        min_lat, min_lon, max_lat, max_lon = bbox

        # Bounding box should contain the center point
        assert min_lat < lat < max_lat
        assert min_lon < lon < max_lon

        # Approximate size check
        lat_diff = max_lat - min_lat
        lon_diff = max_lon - min_lon

        assert lat_diff > 0
        assert lon_diff > 0

    def test_point_in_bbox(self):
        """Test checking if point is in bounding box"""
        center_lat, center_lon = 45.4642, 9.1900
        bbox = get_bounding_box(center_lat, center_lon, 10)

        # Center should be in bbox
        assert is_point_in_bounding_box(center_lat, center_lon, bbox) is True

        # Nearby point should be in bbox
        assert is_point_in_bounding_box(45.47, 9.19, bbox) is True

        # Far point should not be in bbox
        assert is_point_in_bounding_box(46.0, 10.0, bbox) is False

    def test_bbox_at_poles(self):
        """Test bounding box near poles"""
        # Near north pole
        bbox = get_bounding_box(89, 0, 100)
        min_lat, min_lon, max_lat, max_lon = bbox

        # Should be close to 90 (clamped)
        assert max_lat >= 89.9  # Close to pole

        # Near south pole
        bbox = get_bounding_box(-89, 0, 100)
        min_lat, min_lon, max_lat, max_lon = bbox

        # Should be close to -90 (clamped)
        assert min_lat <= -89.9  # Close to pole

    def test_invalid_coordinates_bbox(self):
        """Test bounding box with invalid coordinates"""
        with pytest.raises(ValueError):
            get_bounding_box(91, 0, 10)


class TestBearing:
    """Tests for bearing calculations"""

    def test_north_bearing(self):
        """Test bearing going north"""
        # From equator going north
        b = bearing(0, 0, 1, 0)
        assert abs(b - 0) < 1  # Should be close to 0 (North)

    def test_east_bearing(self):
        """Test bearing going east"""
        # From point going east
        b = bearing(45, 0, 45, 1)
        assert 85 < b < 95  # Should be close to 90 (East)

    def test_south_bearing(self):
        """Test bearing going south"""
        # From point going south
        b = bearing(1, 0, 0, 0)
        assert 175 < b < 185  # Should be close to 180 (South)

    def test_west_bearing(self):
        """Test bearing going west"""
        # From point going west
        b = bearing(45, 1, 45, 0)
        assert 265 < b < 275  # Should be close to 270 (West)

    def test_same_point_bearing(self):
        """Test bearing to same point"""
        # Bearing to same point is undefined, but function should not crash
        b = bearing(45, 9, 45, 9)
        assert 0 <= b < 360

    def test_invalid_coordinates_bearing(self):
        """Test bearing with invalid coordinates"""
        with pytest.raises(ValueError):
            bearing(91, 0, 0, 0)


class TestMidpoint:
    """Tests for midpoint calculations"""

    def test_same_point_midpoint(self):
        """Test midpoint of same point"""
        lat, lon = 45.4642, 9.1900
        mid_lat, mid_lon = midpoint(lat, lon, lat, lon)

        assert abs(mid_lat - lat) < 0.0001
        assert abs(mid_lon - lon) < 0.0001

    def test_equator_midpoint(self):
        """Test midpoint along equator"""
        mid_lat, mid_lon = midpoint(0, 0, 0, 10)

        assert abs(mid_lat - 0) < 0.1  # Should be near equator
        assert abs(mid_lon - 5) < 0.5  # Should be near middle longitude

    def test_milan_rome_midpoint(self):
        """Test midpoint between Milan and Rome"""
        milan_lat, milan_lon = 45.4642, 9.1900
        rome_lat, rome_lon = 41.9028, 12.4964

        mid_lat, mid_lon = midpoint(milan_lat, milan_lon, rome_lat, rome_lon)

        # Midpoint should be between the two cities
        assert min(milan_lat, rome_lat) < mid_lat < max(milan_lat, rome_lat)
        assert min(milan_lon, rome_lon) < mid_lon < max(milan_lon, rome_lon)

    def test_invalid_coordinates_midpoint(self):
        """Test midpoint with invalid coordinates"""
        with pytest.raises(ValueError):
            midpoint(91, 0, 0, 0)
