from sqlalchemy.orm import Session
from pymypersonalmap.models.user import User


def create_user(
    db: Session,
    email: str,
    username: str,
    hashed_password: str,
    full_name: str | None = None,
    is_admin: bool = False
) -> User:
    """Create a new user"""
    user = User(
        email=email,
        username=username,
        hashed_password=hashed_password,
        full_name=full_name,
        is_admin=is_admin
    )
    db.add(user)
    db.flush()  # Assign ID without commit
    return user


def get_user_by_id(db: Session, user_id: int) -> User | None:
    """Get user by ID"""
    return db.get(User, user_id)


def get_user_by_email(db: Session, email: str) -> User | None:
    """Get user by email"""
    return db.query(User).filter(User.email == email).first()


def get_user_by_username(db: Session, username: str) -> User | None:
    """Get user by username"""
    return db.query(User).filter(User.username == username).first()


def get_all_users(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    active_only: bool = False
) -> list[User]:
    """Get all users with pagination"""
    query = db.query(User)
    if active_only:
        query = query.filter(User.is_active == True)
    return query.offset(skip).limit(limit).all()


def update_user(
    db: Session,
    user_id: int,
    email: str | None = None,
    username: str | None = None,
    full_name: str | None = None,
    hashed_password: str | None = None,
    is_active: bool | None = None,
    is_admin: bool | None = None
) -> User | None:
    """Update user fields"""
    user = db.get(User, user_id)
    if not user:
        return None

    if email is not None:
        user.email = email
    if username is not None:
        user.username = username
    if full_name is not None:
        user.full_name = full_name
    if hashed_password is not None:
        user.hashed_password = hashed_password
    if is_active is not None:
        user.is_active = is_active
    if is_admin is not None:
        user.is_admin = is_admin

    db.flush()
    return user


def delete_user(db: Session, user_id: int) -> bool:
    """Delete a user"""
    user = db.get(User, user_id)
    if not user:
        return False

    db.delete(user)
    db.flush()
    return True


def user_exists_by_email(db: Session, email: str) -> bool:
    """Check if user exists by email"""
    return db.query(User).filter(User.email == email).count() > 0


def user_exists_by_username(db: Session, username: str) -> bool:
    """Check if user exists by username"""
    return db.query(User).filter(User.username == username).count() > 0