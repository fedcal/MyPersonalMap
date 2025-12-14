"""
LabelService - Business logic for label operations

Handles label CRUD operations, system label initialization, and validation.
"""

from sqlalchemy.orm import Session
from pymypersonalmap.repository import labels_repository
from pymypersonalmap.models.labels import Label


class LabelNotFoundError(Exception):
    """Raised when label is not found"""
    pass


class LabelAlreadyExistsError(Exception):
    """Raised when trying to create a label that already exists"""
    pass


# System labels defined for the application
SYSTEM_LABELS = [
    {"name": "Urbex", "color": "#8B4513", "icon": "building-slash"},
    {"name": "Ristorante", "color": "#FFC300", "icon": "utensils"},
    {"name": "Fotografia", "color": "#3B82F6", "icon": "camera"},
    {"name": "Drone", "color": "#10B981", "icon": "helicopter"},
    {"name": "Panorama", "color": "#6366F1", "icon": "mountain"},
    {"name": "Storia", "color": "#8B5CF6", "icon": "landmark"},
    {"name": "Natura", "color": "#059669", "icon": "tree"},
    {"name": "Spiaggia", "color": "#06B6D4", "icon": "umbrella-beach"},
    {"name": "Montagna", "color": "#6B7280", "icon": "mountain"},
    {"name": "Città", "color": "#EF4444", "icon": "city"},
]


def initialize_system_labels(db: Session) -> list[Label]:
    """
    Initialize system labels in the database

    Creates default system labels if they don't exist.
    Should be called during database initialization.

    Args:
        db: Database session

    Returns:
        List of created system labels
    """
    existing_labels = labels_repository.get_system_labels(db)
    existing_names = {label.name for label in existing_labels}

    # Filter out labels that already exist
    labels_to_create = [
        label_data for label_data in SYSTEM_LABELS
        if label_data["name"] not in existing_names
    ]

    if not labels_to_create:
        print("System labels already initialized")
        return existing_labels

    # Create missing system labels
    created_labels = labels_repository.bulk_create_system_labels(db, labels_to_create)
    db.commit()

    print(f"Created {len(created_labels)} system labels")
    return created_labels + existing_labels


def create_custom_label(
    db: Session,
    name: str,
    user_id: int,
    color: str = "#3B82F6",
    icon: str | None = None
) -> Label:
    """
    Create a custom user label

    Args:
        db: Database session
        name: Label name
        user_id: ID of user creating the label
        color: Hex color code (default: blue)
        icon: Optional icon name

    Returns:
        Created Label instance

    Raises:
        LabelAlreadyExistsError: If label with this name already exists
        ValueError: If name or color is invalid
    """
    # Validate name
    if not name or len(name.strip()) == 0:
        raise ValueError("Label name cannot be empty")

    if len(name) > 100:
        raise ValueError("Label name cannot exceed 100 characters")

    # Check if label already exists
    if labels_repository.label_exists_by_name(db, name.strip()):
        raise LabelAlreadyExistsError(f"Label '{name}' already exists")

    # Validate color (basic hex color validation)
    if not color.startswith("#") or len(color) != 7:
        raise ValueError("Color must be a valid hex code (e.g., #3B82F6)")

    # Create label
    label = labels_repository.create_label(
        db=db,
        name=name.strip(),
        color=color,
        icon=icon,
        is_system=False,
        created_by=user_id
    )

    db.commit()
    return label


def get_label(db: Session, label_id: int) -> Label:
    """
    Get label by ID

    Args:
        db: Database session
        label_id: Label ID

    Returns:
        Label instance

    Raises:
        LabelNotFoundError: If label not found
    """
    label = labels_repository.get_label_by_id(db, label_id)
    if not label:
        raise LabelNotFoundError(f"Label with ID {label_id} not found")
    return label


def get_available_labels(db: Session, user_id: int | None = None) -> list[Label]:
    """
    Get all labels available to a user

    Returns system labels + user's custom labels.

    Args:
        db: Database session
        user_id: Optional user ID to include their custom labels

    Returns:
        List of available labels
    """
    return labels_repository.get_all_labels(
        db=db,
        user_id=user_id,
        limit=1000  # High limit to get all labels
    )


def get_system_labels(db: Session) -> list[Label]:
    """Get all system labels"""
    return labels_repository.get_system_labels(db)


def get_user_custom_labels(db: Session, user_id: int) -> list[Label]:
    """Get custom labels created by a user"""
    return labels_repository.get_user_labels(db, user_id)


def update_label(
    db: Session,
    label_id: int,
    user_id: int,
    name: str | None = None,
    color: str | None = None,
    icon: str | None = None
) -> Label:
    """
    Update a custom label

    System labels cannot be updated.

    Args:
        db: Database session
        label_id: Label ID to update
        user_id: ID of user attempting the update
        name: New name (optional)
        color: New color (optional)
        icon: New icon (optional)

    Returns:
        Updated Label instance

    Raises:
        LabelNotFoundError: If label not found
        PermissionError: If trying to update system label or label owned by another user
        ValueError: If validation fails
    """
    label = labels_repository.get_label_by_id(db, label_id)
    if not label:
        raise LabelNotFoundError(f"Label with ID {label_id} not found")

    if label.is_system:
        raise PermissionError("Cannot update system labels")

    if label.created_by != user_id:
        raise PermissionError("You don't have permission to update this label")

    # Validate name if provided
    if name is not None:
        if len(name.strip()) == 0:
            raise ValueError("Label name cannot be empty")
        if len(name) > 100:
            raise ValueError("Label name cannot exceed 100 characters")

        # Check if new name conflicts with existing label
        existing = labels_repository.get_label_by_name(db, name.strip())
        if existing and existing.idLabel != label_id:
            raise LabelAlreadyExistsError(f"Label '{name}' already exists")

        name = name.strip()

    # Validate color if provided
    if color is not None:
        if not color.startswith("#") or len(color) != 7:
            raise ValueError("Color must be a valid hex code (e.g., #3B82F6)")

    # Update label
    updated = labels_repository.update_label(
        db=db,
        label_id=label_id,
        name=name,
        color=color,
        icon=icon
    )

    if not updated:
        raise LabelNotFoundError(f"Label with ID {label_id} not found")

    db.commit()
    return updated


def delete_label(db: Session, label_id: int, user_id: int) -> None:
    """
    Delete a custom label

    System labels cannot be deleted.

    Args:
        db: Database session
        label_id: Label ID to delete
        user_id: ID of user attempting the deletion

    Raises:
        LabelNotFoundError: If label not found
        PermissionError: If trying to delete system label or label owned by another user
    """
    label = labels_repository.get_label_by_id(db, label_id)
    if not label:
        raise LabelNotFoundError(f"Label with ID {label_id} not found")

    if label.is_system:
        raise PermissionError("Cannot delete system labels")

    if label.created_by != user_id:
        raise PermissionError("You don't have permission to delete this label")

    # Delete label
    success = labels_repository.delete_label(db, label_id)
    if not success:
        raise LabelNotFoundError(f"Label with ID {label_id} not found")

    db.commit()


def get_label_usage_count(db: Session, label_id: int) -> int:
    """
    Get the number of markers using this label

    Args:
        db: Database session
        label_id: Label ID

    Returns:
        Number of markers with this label
    """
    return labels_repository.count_markers_with_label(db, label_id)
