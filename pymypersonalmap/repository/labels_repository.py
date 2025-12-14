from sqlalchemy.orm import Session
from pymypersonalmap.models.labels import Label


def create_label(
    db: Session,
    name: str,
    color: str = "#3B82F6",
    icon: str | None = None,
    is_system: bool = False,
    created_by: int | None = None
) -> Label:
    """Create a new label"""
    label = Label(
        name=name,
        color=color,
        icon=icon,
        is_system=is_system,
        created_by=created_by
    )
    db.add(label)
    db.flush()
    return label


def get_label_by_id(db: Session, label_id: int) -> Label | None:
    """Get label by ID"""
    return db.get(Label, label_id)


def get_label_by_name(db: Session, name: str) -> Label | None:
    """Get label by name"""
    return db.query(Label).filter(Label.name == name).first()


def get_all_labels(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    system_only: bool = False,
    user_id: int | None = None
) -> list[Label]:
    """Get all labels with optional filters"""
    query = db.query(Label)

    if system_only:
        query = query.filter(Label.is_system == True)
    elif user_id is not None:
        # Get system labels + labels created by this user
        query = query.filter(
            (Label.is_system == True) | (Label.created_by == user_id)
        )

    return query.offset(skip).limit(limit).all()


def get_system_labels(db: Session) -> list[Label]:
    """Get all system labels"""
    return db.query(Label).filter(Label.is_system == True).all()


def get_user_labels(db: Session, user_id: int) -> list[Label]:
    """Get labels created by a specific user"""
    return db.query(Label).filter(Label.created_by == user_id).all()


def update_label(
    db: Session,
    label_id: int,
    name: str | None = None,
    color: str | None = None,
    icon: str | None = None
) -> Label | None:
    """Update label fields (only custom labels can be updated)"""
    label = db.get(Label, label_id)
    if not label or label.is_system:
        return None

    if name is not None:
        label.name = name
    if color is not None:
        label.color = color
    if icon is not None:
        label.icon = icon

    db.flush()
    return label


def delete_label(db: Session, label_id: int) -> bool:
    """Delete a label (only custom labels can be deleted)"""
    label = db.get(Label, label_id)
    if not label or label.is_system:
        return False

    db.delete(label)
    db.flush()
    return True


def label_exists_by_name(db: Session, name: str) -> bool:
    """Check if label exists by name"""
    return db.query(Label).filter(Label.name == name).count() > 0


def count_markers_with_label(db: Session, label_id: int) -> int:
    """Count how many markers use this label"""
    label = db.get(Label, label_id)
    if not label:
        return 0
    return len(label.markers)


def bulk_create_system_labels(db: Session, labels_data: list[dict]) -> list[Label]:
    """
    Create multiple system labels at once
    Used for initial database setup

    labels_data format:
    [
        {"name": "Urbex", "color": "#FF5733", "icon": "building"},
        {"name": "Restaurant", "color": "#FFC300", "icon": "utensils"},
        ...
    ]
    """
    labels = []
    for data in labels_data:
        label = Label(
            name=data["name"],
            color=data.get("color", "#3B82F6"),
            icon=data.get("icon"),
            is_system=True,
            created_by=None
        )
        db.add(label)
        labels.append(label)

    db.flush()
    return labels
