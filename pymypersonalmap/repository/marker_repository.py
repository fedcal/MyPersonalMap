"""
Marker Repository

Data access layer for Marker model operations.
Uses lat/lon columns for coordinate storage.
"""

from sqlalchemy.orm import Session
from sqlalchemy import and_
from pymypersonalmap.models.marker import Marker
from pymypersonalmap.models.labels import Label
from pymypersonalmap.services.geo_utils import haversine_distance, get_bounding_box
from typing import List, Optional


def create_marker(
    db: Session,
    title: str,
    latitude: float,
    longitude: float,
    user_id: int,
    description: Optional[str] = None,
    address: Optional[str] = None,
    metadata: Optional[dict] = None,
    is_favorite: bool = False
) -> Marker:
    """
    Create a new marker in the database

    Args:
        db: Database session
        title: Marker title
        latitude: Latitude coordinate
        longitude: Longitude coordinate
        user_id: ID of the user creating the marker
        description: Optional description
        address: Optional address
        metadata: Optional metadata dictionary
        is_favorite: Favorite flag

    Returns:
        Created Marker instance
    """
    marker = Marker(
        title=title,
        description=description,
        latitude=latitude,
        longitude=longitude,
        address=address,
        marker_metadata=metadata,
        is_favorite=is_favorite,
        user_id=user_id
    )

    db.add(marker)
    db.commit()
    db.refresh(marker)

    return marker


def get_marker_by_id(db: Session, marker_id: int) -> Optional[Marker]:
    """
    Get marker by ID

    Args:
        db: Database session
        marker_id: Marker ID

    Returns:
        Marker instance or None if not found
    """
    return db.query(Marker).filter(Marker.idMarker == marker_id).first()


def get_all_markers(
    db: Session,
    user_id: Optional[int] = None,
    skip: int = 0,
    limit: int = 100
) -> List[Marker]:
    """
    Get all markers, optionally filtered by user

    Args:
        db: Database session
        user_id: Optional user ID to filter by
        skip: Number of records to skip (pagination)
        limit: Maximum number of records to return

    Returns:
        List of Marker instances
    """
    query = db.query(Marker)

    if user_id is not None:
        query = query.filter(Marker.user_id == user_id)

    return query.offset(skip).limit(limit).all()


def update_marker(
    db: Session,
    marker_id: int,
    title: Optional[str] = None,
    description: Optional[str] = None,
    latitude: Optional[float] = None,
    longitude: Optional[float] = None,
    address: Optional[str] = None,
    metadata: Optional[dict] = None,
    is_favorite: Optional[bool] = None
) -> Optional[Marker]:
    """
    Update marker fields

    Args:
        db: Database session
        marker_id: Marker ID to update
        title: New title (optional)
        description: New description (optional)
        latitude: New latitude (optional)
        longitude: New longitude (optional)
        address: New address (optional)
        metadata: New metadata (optional)
        is_favorite: New favorite status (optional)

    Returns:
        Updated Marker instance or None if not found
    """
    marker = get_marker_by_id(db, marker_id)
    if not marker:
        return None

    if title is not None:
        marker.title = title
    if description is not None:
        marker.description = description
    if latitude is not None:
        marker.latitude = latitude
    if longitude is not None:
        marker.longitude = longitude
    if address is not None:
        marker.address = address
    if metadata is not None:
        marker.marker_metadata = metadata
    if is_favorite is not None:
        marker.is_favorite = is_favorite

    db.commit()
    db.refresh(marker)

    return marker


def delete_marker(db: Session, marker_id: int) -> bool:
    """
    Delete marker by ID

    Args:
        db: Database session
        marker_id: Marker ID to delete

    Returns:
        True if deleted, False if not found
    """
    marker = get_marker_by_id(db, marker_id)
    if not marker:
        return False

    db.delete(marker)
    db.commit()

    return True


def get_markers_within_radius(
    db: Session,
    latitude: float,
    longitude: float,
    radius_meters: float,
    user_id: Optional[int] = None
) -> List[Marker]:
    """
    Get markers within a radius from a point using bounding box + Haversine

    This uses a two-step approach:
    1. Query markers in bounding box (fast, uses index)
    2. Filter by exact distance using Haversine formula

    Args:
        db: Database session
        latitude: Center point latitude
        longitude: Center point longitude
        radius_meters: Search radius in meters
        user_id: Optional user ID to filter by

    Returns:
        List of markers within radius, sorted by distance
    """
    # Convert radius to km for bounding box
    radius_km = radius_meters / 1000.0

    # Get bounding box
    bbox = get_bounding_box(latitude, longitude, radius_km)
    min_lat, min_lon, max_lat, max_lon = bbox

    # Query markers in bounding box
    query = db.query(Marker).filter(
        and_(
            Marker.latitude >= min_lat,
            Marker.latitude <= max_lat,
            Marker.longitude >= min_lon,
            Marker.longitude <= max_lon
        )
    )

    if user_id is not None:
        query = query.filter(Marker.user_id == user_id)

    markers = query.all()

    # Filter by exact distance and add distance attribute
    results = []
    for marker in markers:
        distance = haversine_distance(
            latitude, longitude,
            marker.latitude, marker.longitude,
            unit='meters'
        )
        if distance <= radius_meters:
            # Add distance as attribute for sorting/display
            marker.distance = distance
            results.append(marker)

    # Sort by distance
    results.sort(key=lambda m: m.distance)

    return results


def get_markers_in_bounding_box(
    db: Session,
    min_lat: float,
    min_lon: float,
    max_lat: float,
    max_lon: float,
    user_id: Optional[int] = None
) -> List[Marker]:
    """
    Get markers within a bounding box

    Args:
        db: Database session
        min_lat: Minimum latitude
        min_lon: Minimum longitude
        max_lat: Maximum latitude
        max_lon: Maximum longitude
        user_id: Optional user ID to filter by

    Returns:
        List of markers in bounding box
    """
    query = db.query(Marker).filter(
        and_(
            Marker.latitude >= min_lat,
            Marker.latitude <= max_lat,
            Marker.longitude >= min_lon,
            Marker.longitude <= max_lon
        )
    )

    if user_id is not None:
        query = query.filter(Marker.user_id == user_id)

    return query.all()


def get_favorite_markers(
    db: Session,
    user_id: int,
    skip: int = 0,
    limit: int = 100
) -> List[Marker]:
    """
    Get user's favorite markers

    Args:
        db: Database session
        user_id: User ID
        skip: Number of records to skip
        limit: Maximum number of records

    Returns:
        List of favorite markers
    """
    return db.query(Marker).filter(
        and_(
            Marker.user_id == user_id,
            Marker.is_favorite == True
        )
    ).offset(skip).limit(limit).all()


def add_label_to_marker(
    db: Session,
    marker_id: int,
    label_id: int
) -> Optional[Marker]:
    """
    Associate a label with a marker

    Args:
        db: Database session
        marker_id: Marker ID
        label_id: Label ID

    Returns:
        Updated Marker or None if not found
    """
    marker = get_marker_by_id(db, marker_id)
    label = db.query(Label).filter(Label.idLabel == label_id).first()

    if not marker or not label:
        return None

    # Check if label already associated
    if label not in marker.labels:
        marker.labels.append(label)
        db.commit()
        db.refresh(marker)

    return marker


def remove_label_from_marker(
    db: Session,
    marker_id: int,
    label_id: int
) -> Optional[Marker]:
    """
    Remove label association from marker

    Args:
        db: Database session
        marker_id: Marker ID
        label_id: Label ID

    Returns:
        Updated Marker or None if not found
    """
    marker = get_marker_by_id(db, marker_id)
    label = db.query(Label).filter(Label.idLabel == label_id).first()

    if not marker or not label:
        return None

    # Remove label if associated
    if label in marker.labels:
        marker.labels.remove(label)
        db.commit()
        db.refresh(marker)

    return marker


def search_markers(
    db: Session,
    search_term: str,
    user_id: Optional[int] = None,
    skip: int = 0,
    limit: int = 100
) -> List[Marker]:
    """
    Search markers by title or description

    Args:
        db: Database session
        search_term: Search term
        user_id: Optional user ID filter
        skip: Pagination skip
        limit: Pagination limit

    Returns:
        List of matching markers
    """
    search = f"%{search_term}%"
    query = db.query(Marker).filter(
        (Marker.title.ilike(search)) | (Marker.description.ilike(search))
    )

    if user_id is not None:
        query = query.filter(Marker.user_id == user_id)

    return query.offset(skip).limit(limit).all()
