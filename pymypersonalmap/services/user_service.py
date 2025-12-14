"""
UserService - Business logic for user operations

Handles user registration, authentication, password hashing, and user management.
"""

from sqlalchemy.orm import Session
from passlib.context import CryptContext
from pymypersonalmap.repository import user_repository
from pymypersonalmap.models.user import User


# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UserNotFoundError(Exception):
    """Raised when user is not found"""
    pass


class UserAlreadyExistsError(Exception):
    """Raised when trying to create a user that already exists"""
    pass


class InvalidCredentialsError(Exception):
    """Raised when authentication fails"""
    pass


def hash_password(password: str) -> str:
    """
    Hash a password using bcrypt

    Args:
        password: Plain text password

    Returns:
        Hashed password
    """
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a password against a hash

    Args:
        plain_password: Plain text password to verify
        hashed_password: Hashed password to compare against

    Returns:
        True if password matches, False otherwise
    """
    return pwd_context.verify(plain_password, hashed_password)


def create_user(
    db: Session,
    email: str,
    username: str,
    password: str,
    full_name: str | None = None,
    is_admin: bool = False
) -> User:
    """
    Create a new user with password hashing

    Args:
        db: Database session
        email: User email (must be unique)
        username: Username (must be unique)
        password: Plain text password (will be hashed)
        full_name: Optional full name
        is_admin: Whether user should have admin privileges

    Returns:
        Created User instance

    Raises:
        UserAlreadyExistsError: If email or username already exists
        ValueError: If validation fails
    """
    # Validate email
    if not email or len(email.strip()) == 0:
        raise ValueError("Email cannot be empty")

    if len(email) > 255:
        raise ValueError("Email cannot exceed 255 characters")

    if "@" not in email:
        raise ValueError("Invalid email format")

    # Validate username
    if not username or len(username.strip()) == 0:
        raise ValueError("Username cannot be empty")

    if len(username) > 100:
        raise ValueError("Username cannot exceed 100 characters")

    # Validate password
    if not password or len(password) < 8:
        raise ValueError("Password must be at least 8 characters long")

    # Check if user already exists
    if user_repository.user_exists_by_email(db, email.strip()):
        raise UserAlreadyExistsError(f"User with email '{email}' already exists")

    if user_repository.user_exists_by_username(db, username.strip()):
        raise UserAlreadyExistsError(f"User with username '{username}' already exists")

    # Hash password
    hashed_password = hash_password(password)

    # Create user
    user = user_repository.create_user(
        db=db,
        email=email.strip().lower(),
        username=username.strip(),
        hashed_password=hashed_password,
        full_name=full_name.strip() if full_name else None,
        is_admin=is_admin
    )

    db.commit()
    return user


def authenticate_user(
    db: Session,
    email: str,
    password: str
) -> User:
    """
    Authenticate a user with email and password

    Args:
        db: Database session
        email: User email
        password: Plain text password

    Returns:
        User instance if authentication successful

    Raises:
        InvalidCredentialsError: If credentials are invalid
    """
    user = user_repository.get_user_by_email(db, email.strip().lower())

    if not user:
        raise InvalidCredentialsError("Invalid email or password")

    if not user.is_active:
        raise InvalidCredentialsError("User account is inactive")

    if not verify_password(password, user.hashed_password):
        raise InvalidCredentialsError("Invalid email or password")

    return user


def get_user_by_id(db: Session, user_id: int) -> User:
    """
    Get user by ID

    Args:
        db: Database session
        user_id: User ID

    Returns:
        User instance

    Raises:
        UserNotFoundError: If user not found
    """
    user = user_repository.get_user_by_id(db, user_id)
    if not user:
        raise UserNotFoundError(f"User with ID {user_id} not found")
    return user


def get_user_by_email(db: Session, email: str) -> User:
    """
    Get user by email

    Args:
        db: Database session
        email: User email

    Returns:
        User instance

    Raises:
        UserNotFoundError: If user not found
    """
    user = user_repository.get_user_by_email(db, email.strip().lower())
    if not user:
        raise UserNotFoundError(f"User with email '{email}' not found")
    return user


def get_user_by_username(db: Session, username: str) -> User:
    """
    Get user by username

    Args:
        db: Database session
        username: Username

    Returns:
        User instance

    Raises:
        UserNotFoundError: If user not found
    """
    user = user_repository.get_user_by_username(db, username.strip())
    if not user:
        raise UserNotFoundError(f"User with username '{username}' not found")
    return user


def get_all_users(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    active_only: bool = True
) -> list[User]:
    """Get all users with pagination"""
    return user_repository.get_all_users(
        db=db,
        skip=skip,
        limit=limit,
        active_only=active_only
    )


def update_user_profile(
    db: Session,
    user_id: int,
    email: str | None = None,
    username: str | None = None,
    full_name: str | None = None
) -> User:
    """
    Update user profile information

    Args:
        db: Database session
        user_id: User ID to update
        email: New email (optional)
        username: New username (optional)
        full_name: New full name (optional)

    Returns:
        Updated User instance

    Raises:
        UserNotFoundError: If user not found
        UserAlreadyExistsError: If new email/username conflicts
        ValueError: If validation fails
    """
    user = user_repository.get_user_by_id(db, user_id)
    if not user:
        raise UserNotFoundError(f"User with ID {user_id} not found")

    # Validate and check email if provided
    if email is not None:
        if "@" not in email:
            raise ValueError("Invalid email format")
        email_clean = email.strip().lower()
        if email_clean != user.email:
            if user_repository.user_exists_by_email(db, email_clean):
                raise UserAlreadyExistsError(f"Email '{email}' already in use")
            email = email_clean
        else:
            email = None  # No change needed

    # Validate and check username if provided
    if username is not None:
        username_clean = username.strip()
        if username_clean != user.username:
            if user_repository.user_exists_by_username(db, username_clean):
                raise UserAlreadyExistsError(f"Username '{username}' already in use")
            username = username_clean
        else:
            username = None  # No change needed

    # Update user
    updated = user_repository.update_user(
        db=db,
        user_id=user_id,
        email=email,
        username=username,
        full_name=full_name.strip() if full_name else None
    )

    if not updated:
        raise UserNotFoundError(f"User with ID {user_id} not found")

    db.commit()
    return updated


def change_password(
    db: Session,
    user_id: int,
    current_password: str,
    new_password: str
) -> User:
    """
    Change user password

    Args:
        db: Database session
        user_id: User ID
        current_password: Current password for verification
        new_password: New password

    Returns:
        Updated User instance

    Raises:
        UserNotFoundError: If user not found
        InvalidCredentialsError: If current password is incorrect
        ValueError: If new password is invalid
    """
    user = user_repository.get_user_by_id(db, user_id)
    if not user:
        raise UserNotFoundError(f"User with ID {user_id} not found")

    # Verify current password
    if not verify_password(current_password, user.hashed_password):
        raise InvalidCredentialsError("Current password is incorrect")

    # Validate new password
    if len(new_password) < 8:
        raise ValueError("New password must be at least 8 characters long")

    # Hash new password
    hashed_password = hash_password(new_password)

    # Update password
    updated = user_repository.update_user(
        db=db,
        user_id=user_id,
        hashed_password=hashed_password
    )

    if not updated:
        raise UserNotFoundError(f"User with ID {user_id} not found")

    db.commit()
    return updated


def deactivate_user(db: Session, user_id: int) -> User:
    """
    Deactivate a user account

    Args:
        db: Database session
        user_id: User ID to deactivate

    Returns:
        Updated User instance

    Raises:
        UserNotFoundError: If user not found
    """
    updated = user_repository.update_user(
        db=db,
        user_id=user_id,
        is_active=False
    )

    if not updated:
        raise UserNotFoundError(f"User with ID {user_id} not found")

    db.commit()
    return updated


def activate_user(db: Session, user_id: int) -> User:
    """
    Activate a user account

    Args:
        db: Database session
        user_id: User ID to activate

    Returns:
        Updated User instance

    Raises:
        UserNotFoundError: If user not found
    """
    updated = user_repository.update_user(
        db=db,
        user_id=user_id,
        is_active=True
    )

    if not updated:
        raise UserNotFoundError(f"User with ID {user_id} not found")

    db.commit()
    return updated


def delete_user(db: Session, user_id: int) -> None:
    """
    Permanently delete a user

    Warning: This will also delete all associated markers due to CASCADE.

    Args:
        db: Database session
        user_id: User ID to delete

    Raises:
        UserNotFoundError: If user not found
    """
    success = user_repository.delete_user(db, user_id)
    if not success:
        raise UserNotFoundError(f"User with ID {user_id} not found")

    db.commit()
