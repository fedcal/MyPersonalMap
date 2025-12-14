from datetime import datetime
from sqlalchemy import ForeignKey, DateTime, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func

from pymypersonalmap.database.session import Base


class MarkerLabel(Base):
    """
    Association table for many-to-many relationship between Markers and Labels
    """
    __tablename__ = "marker_labels"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True
    )

    marker_id: Mapped[int] = mapped_column(
        ForeignKey("markers.idMarker", ondelete="CASCADE"),
        nullable=False
    )

    label_id: Mapped[int] = mapped_column(
        ForeignKey("labels.idLabel", ondelete="CASCADE"),
        nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=func.now(),
        nullable=False
    )

    # Ensure a marker can't have the same label multiple times
    __table_args__ = (
        UniqueConstraint('marker_id', 'label_id', name='uq_marker_label'),
    )
