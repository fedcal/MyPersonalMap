from datetime import datetime
from typing import TYPE_CHECKING
from sqlalchemy import String, DateTime, ForeignKey, JSON, Column, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from geoalchemy2 import Geometry

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

    # Spatial column for geographic coordinates (POINT with WGS84 SRID 4326)
    coordinates = Column(
        Geometry(geometry_type='POINT', srid=4326),
        nullable=False
    )

    # JSON metadata for flexible additional data (hours, phone, website, etc.)
    # Using 'marker_metadata' instead of 'metadata' (which is reserved in SQLAlchemy)
    marker_metadata = Column(
        JSON,
        nullable=True
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