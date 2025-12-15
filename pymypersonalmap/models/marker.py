from datetime import datetime
from typing import TYPE_CHECKING
from sqlalchemy import String, DateTime, ForeignKey, JSON, Column, Text, Float, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from pymypersonalmap.database.session import Base

if TYPE_CHECKING:
    from pymypersonalmap.models.user import User
    from pymypersonalmap.models.labels import Label


class Marker(Base):
    __tablename__ = "markers"

    idMarker: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True
    )

    title: Mapped[str] = mapped_column(
        String(200),
        nullable=False
    )

    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )

    # Geographic coordinates using WGS84 (EPSG:4326)
    # Stored as separate latitude/longitude columns for SQLite compatibility
    latitude: Mapped[float] = mapped_column(
        Float,
        nullable=False,
        doc="Latitude in decimal degrees (-90 to +90)"
    )

    longitude: Mapped[float] = mapped_column(
        Float,
        nullable=False,
        doc="Longitude in decimal degrees (-180 to +180)"
    )

    # Optional address for geocoding reference
    address: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True,
        doc="Human-readable address"
    )

    # JSON metadata for flexible additional data (hours, phone, website, etc.)
    # Using 'marker_metadata' instead of 'metadata' (which is reserved in SQLAlchemy)
    marker_metadata = Column(
        JSON,
        nullable=True
    )

    # Favorite flag for quick access
    is_favorite: Mapped[bool] = mapped_column(
        default=False,
        nullable=False
    )

    # Foreign key to user
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.idUser", ondelete="CASCADE"),
        nullable=False
    )

    # Timestamps
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=func.now(),
        nullable=False
    )

    updated_at: Mapped[datetime | None] = mapped_column(
        DateTime,
        onupdate=func.now(),
        nullable=True
    )

    # Relationships
    user: Mapped["User"] = relationship(
        "User",
        back_populates="markers"
    )

    labels: Mapped[list["Label"]] = relationship(
        "Label",
        secondary="marker_labels",
        back_populates="markers"
    )

    # Indexes for performance
    __table_args__ = (
        # Compound index for geographic queries (bounding box searches)
        Index('idx_marker_coordinates', 'latitude', 'longitude'),
        # Index for favorite markers
        Index('idx_marker_favorite', 'is_favorite'),
        # Index for user queries
        Index('idx_marker_user', 'user_id'),
    )

    def __repr__(self) -> str:
        return f"<Marker(id={self.idMarker}, title='{self.title}', lat={self.latitude}, lon={self.longitude})>"

    @property
    def coordinates_tuple(self) -> tuple[float, float]:
        """Return coordinates as (latitude, longitude) tuple"""
        return (self.latitude, self.longitude)

    def to_dict(self) -> dict:
        """Convert marker to dictionary for API responses"""
        return {
            'id': self.idMarker,
            'title': self.title,
            'description': self.description,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'address': self.address,
            'metadata': self.marker_metadata,
            'is_favorite': self.is_favorite,
            'user_id': self.user_id,
            'labels': [label.name for label in self.labels] if self.labels else [],
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
        }