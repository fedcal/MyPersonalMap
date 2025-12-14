from sqlalchemy.orm import Session
from geoalchemy2.functions import ST_Distance_Sphere, ST_MakePoint
from geoalchemy2.elements import WKTElement
from pymypersonalmap.models.marker import Marker
from pymypersonalmap.models.labels import Label


def create_marker(
    db: Session,
    title: str,
    latitude: float,
    longitude: float,
    user_id: int,
    description: str | None = None,
    metadata: dict | None = None
) -> Marker:
    """Create a new marker with geographic coordinates"""
    # Create POINT geometry from lat/lon
    point = WKTElement(f'POINT({longitude} {latitude})', srid=4326)

    marker = Marker(
        title=title,
        description=description,
        coordinates=point,
        metadata=metadata,
        user_id=user_id
    )
    db.add(marker)
    db.flush()
    return marker


def get_marker_by_id(db: Session, marker_id: int) -> Marker | None:
    """Get marker by ID"""
    return db.get(Marker, marker_id)


def get_all_markers(
    db: Session,
    user_id: int | None = None,
    skip: int = 0,
    limit: int = 100
) -> list[Marker]:
    """Get all markers with optional user filter and pagination"""
    query = db.query(Marker)
    if user_id is not None:
        query = query.filter(Marker.user_id == user_id)
    return query.offset(skip).limit(limit).all()


def get_markers_by_label(
    db: Session,
    label_id: int,
    user_id: int | None = None,
    skip: int = 0,
    limit: int = 100
) -> list[Marker]:
    """Get markers filtered by label"""
    query = db.query(Marker).join(Marker.labels).filter(Label.idLabel == label_id)
    if user_id is not None:
        query = query.filter(Marker.user_id == user_id)
    return query.offset(skip).limit(limit).all()


def get_markers_within_radius(
    db: Session,
    latitude: float,
    longitude: float,
    radius_meters: float,
    user_id: int | None = None
) -> list[Marker]:
    """
    Get markers within a given radius (in meters) from a point
    Uses ST_Distance_Sphere for accurate distance calculation
    """
    point = ST_MakePoint(longitude, latitude)
    query = db.query(Marker).filter(
        ST_Distance_Sphere(Marker.coordinates, point) <= radius_meters
    )
    if user_id is not None:
        query = query.filter(Marker.user_id == user_id)
    return query.all()


def get_markers_in_bounding_box(
    db: Session,
    min_lat: float,
    min_lon: float,
    max_lat: float,
    max_lon: float,
    user_id: int | None = None
) -> list[Marker]:
    """Get markers within a geographic bounding box"""
    # Using ST_DWithin with a large enough distance to cover the bounding box
    # Alternative: use ST_MakeEnvelope and ST_Contains for exact bounding box
    query = db.query(Marker).filter(
        Marker.coordinates.ST_X().between(min_lon, max_lon),
        Marker.coordinates.ST_Y().between(min_lat, max_lat)
    )
    if user_id is not None:
        query = query.filter(Marker.user_id == user_id)
    return query.all()


def update_marker(
    db: Session,
    marker_id: int,
    title: str | None = None,
    description: str | None = None,
    latitude: float | None = None,
    longitude: float | None = None,
    metadata: dict | None = None
) -> Marker | None:
    """Update marker fields"""
    marker = db.get(Marker, marker_id)
    if not marker:
        return None

    if title is not None:
        marker.title = title
    if description is not None:
        marker.description = description
    if latitude is not None and longitude is not None:
        # Update coordinates
        point = WKTElement(f'POINT({longitude} {latitude})', srid=4326)
        marker.coordinates = point
    if metadata is not None:
        marker.metadata = metadata

    db.flush()
    return marker


def delete_marker(db: Session, marker_id: int) -> bool:
    """Delete a marker"""
    marker = db.get(Marker, marker_id)
    if not marker:
        return False

    db.delete(marker)
    db.flush()
    return True


def add_label_to_marker(
    db: Session,
    marker_id: int,
    label_id: int
) -> Marker | None:
    """Add a label to a marker"""
    marker = db.get(Marker, marker_id)
    label = db.get(Label, label_id)

    if not marker or not label:
        return None

    if label not in marker.labels:
        marker.labels.append(label)
        db.flush()

    return marker


def remove_label_from_marker(
    db: Session,
    marker_id: int,
    label_id: int
) -> Marker | None:
    """Remove a label from a marker"""
    marker = db.get(Marker, marker_id)
    label = db.get(Label, label_id)

    if not marker or not label:
        return None

    if label in marker.labels:
        marker.labels.remove(label)
        db.flush()

    return marker


def count_markers_by_user(db: Session, user_id: int) -> int:
    """Count markers for a specific user"""
    return db.query(Marker).filter(Marker.user_id == user_id).count()
