from datetime import datetime
from typing import TYPE_CHECKING
from sqlalchemy import String, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from pymypersonalmap.database.session import Base

if TYPE_CHECKING:
    from pymypersonalmap.models.marker import Marker
    from pymypersonalmap.models.user import User


class Label(Base):
    __tablename__ = "labels"

    idLabel: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True
    )

    name: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        nullable=False,
        index=True
    )

    color: Mapped[str] = mapped_column(
        String(7),  # Hex color format #RRGGBB
        nullable=False,
        default="#3B82F6"  # Blue
    )

    icon: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True
    )

    is_system: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False
    )

    created_by: Mapped[int | None] = mapped_column(
        ForeignKey("users.idUser", ondelete="SET NULL"),
        nullable=True
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=func.now(),
        nullable=False
    )

    # Relationships
    markers: Mapped[list["Marker"]] = relationship(
        "Marker",
        secondary="marker_labels",
        back_populates="labels"
    )

    creator: Mapped["User | None"] = relationship(
        "User",
        foreign_keys=[created_by]
    )