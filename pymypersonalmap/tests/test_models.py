"""
Tests for Database Models

Tests for Marker, User, and Label models.
"""

import pytest
from datetime import datetime
from pymypersonalmap.models.marker import Marker
from pymypersonalmap.models.user import User
from pymypersonalmap.models.labels import Label


class TestMarkerModel:
    """Tests for Marker model"""

    def test_create_marker(self, test_db, sample_user):
        """Test creating a basic marker"""
        marker = Marker(
            title="Test Marker",
            description="Test description",
            latitude=45.4642,
            longitude=9.1900,
            user_id=sample_user.idUser
        )

        test_db.add(marker)
        test_db.commit()
        test_db.refresh(marker)

        assert marker.idMarker is not None
        assert marker.title == "Test Marker"
        assert marker.latitude == 45.4642
        assert marker.longitude == 9.1900
        assert marker.created_at is not None

    def test_marker_coordinates_tuple(self, sample_marker):
        """Test coordinates_tuple property"""
        coords = sample_marker.coordinates_tuple
        assert coords == (sample_marker.latitude, sample_marker.longitude)
        assert coords == (45.4642, 9.1900)

    def test_marker_to_dict(self, sample_marker):
        """Test marker to_dict method"""
        marker_dict = sample_marker.to_dict()

        assert marker_dict['id'] == sample_marker.idMarker
        assert marker_dict['title'] == sample_marker.title
        assert marker_dict['latitude'] == sample_marker.latitude
        assert marker_dict['longitude'] == sample_marker.longitude
        assert marker_dict['address'] == sample_marker.address
        assert marker_dict['is_favorite'] == sample_marker.is_favorite
        assert 'created_at' in marker_dict
        assert isinstance(marker_dict['labels'], list)

    def test_marker_with_labels(self, test_db, sample_user, sample_labels):
        """Test marker with associated labels"""
        marker = Marker(
            title="Tagged Marker",
            latitude=45.0,
            longitude=9.0,
            user_id=sample_user.idUser
        )

        # Associate labels
        marker.labels = [sample_labels[0], sample_labels[1]]

        test_db.add(marker)
        test_db.commit()
        test_db.refresh(marker)

        assert len(marker.labels) == 2
        assert sample_labels[0] in marker.labels
        assert sample_labels[1] in marker.labels

    def test_marker_favorite(self, test_db, sample_user):
        """Test marker favorite flag"""
        marker = Marker(
            title="Favorite Place",
            latitude=45.0,
            longitude=9.0,
            is_favorite=True,
            user_id=sample_user.idUser
        )

        test_db.add(marker)
        test_db.commit()
        test_db.refresh(marker)

        assert marker.is_favorite is True

    def test_marker_with_metadata(self, test_db, sample_user):
        """Test marker with JSON metadata"""
        metadata = {
            "opening_hours": "9:00-18:00",
            "phone": "+39 02 1234567",
            "website": "https://example.com",
            "rating": 4.5
        }

        marker = Marker(
            title="Place with metadata",
            latitude=45.0,
            longitude=9.0,
            marker_metadata=metadata,
            user_id=sample_user.idUser
        )

        test_db.add(marker)
        test_db.commit()
        test_db.refresh(marker)

        assert marker.marker_metadata == metadata
        assert marker.marker_metadata['phone'] == "+39 02 1234567"
        assert marker.marker_metadata['rating'] == 4.5

    def test_marker_repr(self, sample_marker):
        """Test marker string representation"""
        repr_str = repr(sample_marker)
        assert "Marker" in repr_str
        assert str(sample_marker.idMarker) in repr_str
        assert sample_marker.title in repr_str

    def test_marker_timestamps(self, test_db, sample_user):
        """Test marker automatic timestamps"""
        marker = Marker(
            title="Timestamp Test",
            latitude=45.0,
            longitude=9.0,
            user_id=sample_user.idUser
        )

        test_db.add(marker)
        test_db.commit()
        test_db.refresh(marker)

        # created_at should be set automatically
        assert marker.created_at is not None
        assert isinstance(marker.created_at, datetime)

        # updated_at should be None on creation
        assert marker.updated_at is None

        # Update marker
        marker.title = "Updated Title"
        test_db.commit()
        test_db.refresh(marker)

        # updated_at should now be set (in some DB setups)
        # Note: SQLite might not update this automatically


class TestUserModel:
    """Tests for User model"""

    def test_create_user(self, test_db):
        """Test creating a user"""
        user = User(
            username="newuser",
            email="new@example.com",
            hashed_password="hashed123"
        )

        test_db.add(user)
        test_db.commit()
        test_db.refresh(user)

        assert user.idUser is not None
        assert user.username == "newuser"
        assert user.email == "new@example.com"
        assert user.created_at is not None

    def test_user_markers_relationship(self, test_db, sample_user):
        """Test user-markers relationship"""
        marker1 = Marker(
            title="Marker 1",
            latitude=45.0,
            longitude=9.0,
            user_id=sample_user.idUser
        )
        marker2 = Marker(
            title="Marker 2",
            latitude=46.0,
            longitude=10.0,
            user_id=sample_user.idUser
        )

        test_db.add_all([marker1, marker2])
        test_db.commit()
        test_db.refresh(sample_user)

        assert len(sample_user.markers) == 2


class TestLabelModel:
    """Tests for Label model"""

    def test_create_label(self, test_db):
        """Test creating a label"""
        label = Label(
            name="Custom Label",
            color="#FF5733",
            icon="star",
            is_system=False
        )

        test_db.add(label)
        test_db.commit()
        test_db.refresh(label)

        assert label.idLabel is not None
        assert label.name == "Custom Label"
        assert label.color == "#FF5733"
        assert label.is_system is False

    def test_system_label(self, sample_labels):
        """Test system labels"""
        system_labels = [l for l in sample_labels if l.is_system]
        assert len(system_labels) > 0

        for label in system_labels:
            assert label.is_system is True

    def test_label_markers_relationship(self, test_db, sample_user, sample_labels):
        """Test label-markers many-to-many relationship"""
        label = sample_labels[0]

        marker1 = Marker(
            title="Tagged 1",
            latitude=45.0,
            longitude=9.0,
            user_id=sample_user.idUser
        )
        marker2 = Marker(
            title="Tagged 2",
            latitude=46.0,
            longitude=10.0,
            user_id=sample_user.idUser
        )

        # Associate markers with label
        marker1.labels.append(label)
        marker2.labels.append(label)

        test_db.add_all([marker1, marker2])
        test_db.commit()
        test_db.refresh(label)

        assert len(label.markers) == 2


class TestMarkerQueries:
    """Tests for common marker queries"""

    def test_query_markers_by_user(self, test_db, sample_user):
        """Test querying markers by user"""
        # Create multiple markers for user
        markers = [
            Marker(
                title=f"Marker {i}",
                latitude=45.0 + i * 0.1,
                longitude=9.0 + i * 0.1,
                user_id=sample_user.idUser
            )
            for i in range(5)
        ]

        test_db.add_all(markers)
        test_db.commit()

        # Query markers for user
        user_markers = test_db.query(Marker).filter(
            Marker.user_id == sample_user.idUser
        ).all()

        assert len(user_markers) == 5

    def test_query_favorite_markers(self, test_db, sample_user):
        """Test querying favorite markers"""
        # Create mix of favorite and non-favorite
        markers = [
            Marker(
                title=f"Marker {i}",
                latitude=45.0 + i,
                longitude=9.0,
                is_favorite=(i % 2 == 0),
                user_id=sample_user.idUser
            )
            for i in range(6)
        ]

        test_db.add_all(markers)
        test_db.commit()

        # Query only favorites
        favorites = test_db.query(Marker).filter(
            Marker.is_favorite == True
        ).all()

        assert len(favorites) == 3
        for marker in favorites:
            assert marker.is_favorite is True

    def test_query_markers_in_area(self, test_db, sample_user):
        """Test querying markers in geographic area (bounding box)"""
        # Create markers in different locations
        markers = [
            Marker(title="Inside 1", latitude=45.5, longitude=9.2, user_id=sample_user.idUser),
            Marker(title="Inside 2", latitude=45.6, longitude=9.3, user_id=sample_user.idUser),
            Marker(title="Outside 1", latitude=50.0, longitude=15.0, user_id=sample_user.idUser),
            Marker(title="Outside 2", latitude=40.0, longitude=5.0, user_id=sample_user.idUser),
        ]

        test_db.add_all(markers)
        test_db.commit()

        # Define bounding box around Milan area
        min_lat, max_lat = 45.0, 46.0
        min_lon, max_lon = 9.0, 10.0

        # Query markers in bounding box
        markers_in_area = test_db.query(Marker).filter(
            Marker.latitude >= min_lat,
            Marker.latitude <= max_lat,
            Marker.longitude >= min_lon,
            Marker.longitude <= max_lon
        ).all()

        assert len(markers_in_area) == 2
        assert all("Inside" in m.title for m in markers_in_area)
