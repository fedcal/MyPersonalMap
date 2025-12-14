"""
MarkerService - Business logic for marker operations

Handles coordinate validation, marker CRUD operations, and spatial queries.
"""

from sqlalchemy.orm import Session
from pymypersonalmap.repository import marker_repository
from pymypersonalmap.models.marker import Marker


class CoordinateValidationError(Exception):
    """Raised when coordinates are invalid"""
    pass


class MarkerNotFoundError(Exception):
    """Raised when marker is not found"""
    pass


def validate_coordinates(latitude: float, longitude: float) -> None:
    """
    Validate geographic coordinates

    Args:
        latitude: Latitude in decimal degrees
        longitude: Longitude in decimal degrees

    Raises:
        CoordinateValidationError: If coordinates are out of valid range
    """
    if not -90 <= latitude <= 90:
        raise CoordinateValidationError(
            f"Invalid latitude: {latitude}. Must be between -90 and 90."
        )
    if not -180 <= longitude <= 180:
        raise CoordinateValidationError(
            f"Invalid longitude: {longitude}. Must be between -180 and 180."
        )


def create_marker(
    db: Session,
    title: str,
    latitude: float,
    longitude: float,
    user_id: int,
    description: str | None = None,
    metadata: dict | None = None
) -> Marker:
    """
    Create a new marker with validation

    Args:
        db: Database session
        title: Marker title
        latitude: Latitude coordinate
        longitude: Longitude coordinate
        user_id: ID of the user creating the marker
        description: Optional description
        metadata: Optional metadata dictionary

    Returns:
        Created Marker instance

    Raises:
        CoordinateValidationError: If coordinates are invalid
    """
    # Validate coordinates
    validate_coordinates(latitude, longitude)

    # Validate title
    if not title or len(title.strip()) == 0:
        raise ValueError("Title cannot be empty")

    if len(title) > 200:
        raise ValueError("Title cannot exceed 200 characters")

    # Create marker
    return marker_repository.create_marker(
        db=db,
        title=title.strip(),
        latitude=latitude,
        longitude=longitude,
        user_id=user_id,
        description=description.strip() if description else None,
        metadata=metadata
    )


def get_marker(db: Session, marker_id: int) -> Marker:
    """
    Get marker by ID

    Args:
        db: Database session
        marker_id: Marker ID

    Returns:
        Marker instance

    Raises:
        MarkerNotFoundError: If marker not found
    """
    marker = marker_repository.get_marker_by_id(db, marker_id)
    if not marker:
        raise MarkerNotFoundError(f"Marker with ID {marker_id} not found")
    return marker


def get_user_markers(
    db: Session,
    user_id: int,
    skip: int = 0,
    limit: int = 100
) -> list[Marker]:
    """Get all markers for a user"""
    return marker_repository.get_all_markers(
        db=db,
        user_id=user_id,
        skip=skip,
        limit=limit
    )


def update_marker(
    db: Session,
    marker_id: int,
    user_id: int,
    title: str | None = None,
    description: str | None = None,
    latitude: float | None = None,
    longitude: float | None = None,
    metadata: dict | None = None
) -> Marker:
    """
    Update marker with validation and ownership check

    Args:
        db: Database session
        marker_id: Marker ID to update
        user_id: ID of user attempting the update
        title: New title (optional)
        description: New description (optional)
        latitude: New latitude (optional)
        longitude: New longitude (optional)
        metadata: New metadata (optional)

    Returns:
        Updated Marker instance

    Raises:
        MarkerNotFoundError: If marker not found
        PermissionError: If user doesn't own the marker
        CoordinateValidationError: If new coordinates are invalid
    """
    # Check marker exists and user owns it
    marker = marker_repository.get_marker_by_id(db, marker_id)
    if not marker:
        raise MarkerNotFoundError(f"Marker with ID {marker_id} not found")

    if marker.user_id != user_id:
        raise PermissionError("You don't have permission to update this marker")

    # Validate coordinates if provided
    if latitude is not None and longitude is not None:
        validate_coordinates(latitude, longitude)

    # Validate title if provided
    if title is not None:
        if len(title.strip()) == 0:
            raise ValueError("Title cannot be empty")
        if len(title) > 200:
            raise ValueError("Title cannot exceed 200 characters")
        title = title.strip()

    # Update marker
    updated = marker_repository.update_marker(
        db=db,
        marker_id=marker_id,
        title=title,
        description=description.strip() if description else None,
        latitude=latitude,
        longitude=longitude,
        metadata=metadata
    )

    if not updated:
        raise MarkerNotFoundError(f"Marker with ID {marker_id} not found")

    return updated


def delete_marker(db: Session, marker_id: int, user_id: int) -> None:
    """
    Delete marker with ownership check

    Args:
        db: Database session
        marker_id: Marker ID to delete
        user_id: ID of user attempting the deletion

    Raises:
        MarkerNotFoundError: If marker not found
        PermissionError: If user doesn't own the marker
    """
    # Check marker exists and user owns it
    marker = marker_repository.get_marker_by_id(db, marker_id)
    if not marker:
        raise MarkerNotFoundError(f"Marker with ID {marker_id} not found")

    if marker.user_id != user_id:
        raise PermissionError("You don't have permission to delete this marker")

    # Delete marker
    marker_repository.delete_marker(db, marker_id)


def find_markers_nearby(
    db: Session,
    latitude: float,
    longitude: float,
    radius_meters: float,
    user_id: int | None = None
) -> list[Marker]:
    """
    Find markers within a radius from a point

    Args:
        db: Database session
        latitude: Center point latitude
        longitude: Center point longitude
        radius_meters: Search radius in meters
        user_id: Optional user ID to filter results

    Returns:
        List of markers within radius

    Raises:
        CoordinateValidationError: If coordinates are invalid
        ValueError: If radius is invalid
    """
    validate_coordinates(latitude, longitude)

    if radius_meters <= 0:
        raise ValueError("Radius must be positive")

    if radius_meters > 100000:  # 100km limit
        raise ValueError("Radius cannot exceed 100,000 meters (100km)")

    return marker_repository.get_markers_within_radius(
        db=db,
        latitude=latitude,
        longitude=longitude,
        radius_meters=radius_meters,
        user_id=user_id
    )


def find_markers_in_area(
    db: Session,
    min_lat: float,
    min_lon: float,
    max_lat: float,
    max_lon: float,
    user_id: int | None = None
) -> list[Marker]:
    """
    Find markers within a bounding box

    Args:
        db: Database session
        min_lat: Minimum latitude
        min_lon: Minimum longitude
        max_lat: Maximum latitude
        max_lon: Maximum longitude
        user_id: Optional user ID to filter results

    Returns:
        List of markers within bounding box

    Raises:
        CoordinateValidationError: If coordinates are invalid
    """
    validate_coordinates(min_lat, min_lon)
    validate_coordinates(max_lat, max_lon)

    if min_lat >= max_lat:
        raise ValueError("min_lat must be less than max_lat")
    if min_lon >= max_lon:
        raise ValueError("min_lon must be less than max_lon")

    return marker_repository.get_markers_in_bounding_box(
        db=db,
        min_lat=min_lat,
        min_lon=min_lon,
        max_lat=max_lat,
        max_lon=max_lon,
        user_id=user_id
    )


def add_label_to_marker(
    db: Session,
    marker_id: int,
    label_id: int,
    user_id: int
) -> Marker:
    """
    Add a label to a marker with ownership check

    Args:
        db: Database session
        marker_id: Marker ID
        label_id: Label ID to add
        user_id: ID of user attempting the operation

    Returns:
        Updated Marker instance

    Raises:
        MarkerNotFoundError: If marker not found
        PermissionError: If user doesn't own the marker
    """
    # Check marker exists and user owns it
    marker = marker_repository.get_marker_by_id(db, marker_id)
    if not marker:
        raise MarkerNotFoundError(f"Marker with ID {marker_id} not found")

    if marker.user_id != user_id:
        raise PermissionError("You don't have permission to modify this marker")

    # Add label
    result = marker_repository.add_label_to_marker(db, marker_id, label_id)
    if not result:
        raise ValueError(f"Failed to add label {label_id} to marker {marker_id}")

    return result


def remove_label_from_marker(
    db: Session,
    marker_id: int,
    label_id: int,
    user_id: int
) -> Marker:
    """
    Remove a label from a marker with ownership check

    Args:
        db: Database session
        marker_id: Marker ID
        label_id: Label ID to remove
        user_id: ID of user attempting the operation

    Returns:
        Updated Marker instance

    Raises:
        MarkerNotFoundError: If marker not found
        PermissionError: If user doesn't own the marker
    """
    # Check marker exists and user owns it
    marker = marker_repository.get_marker_by_id(db, marker_id)
    if not marker:
        raise MarkerNotFoundError(f"Marker with ID {marker_id} not found")

    if marker.user_id != user_id:
        raise PermissionError("You don't have permission to modify this marker")

    # Remove label
    result = marker_repository.remove_label_from_marker(db, marker_id, label_id)
    if not result:
        raise ValueError(f"Failed to remove label {label_id} from marker {marker_id}")

    return result
