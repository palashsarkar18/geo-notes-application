import pytest
from django.core.exceptions import ValidationError
from pois.models import PointOfInterest
from accounts.models import User


@pytest.mark.django_db
def test_poi_creation():
    user = User.objects.create_user(username='testuser',
                                    password='testpassword',
                                    email='testuser@example.com')
    poi = PointOfInterest.objects.create(
        user=user,
        latitude=45.0,
        longitude=90.0,
        description='A test point of interest'
    )
    assert poi.user == user
    assert poi.username == 'testuser'
    assert poi.latitude == 45.0
    assert poi.longitude == 90.0
    assert poi.description == 'A test point of interest'


@pytest.mark.django_db
def test_invalid_latitude():
    user = User.objects.create_user(username='testuser',
                                    password='testpassword',
                                    email='testuser@example.com')
    with pytest.raises(ValidationError):
        poi = PointOfInterest(
            user=user,
            description='Invalid latitude',
            latitude=95.0,  # Invalid latitude
            longitude=90.0
        )
        poi.full_clean()  # This will trigger the validation


@pytest.mark.django_db
def test_invalid_longitude():
    user = User.objects.create_user(username='testuser',
                                    password='testpassword',
                                    email='testuser@example.com')
    with pytest.raises(ValidationError):
        poi = PointOfInterest(
            user=user,
            description='Invalid longitude',
            latitude=45.0,
            longitude=190.0  # Invalid longitude
        )
        poi.full_clean()  # This will trigger the validation


@pytest.mark.django_db
def test_valid_latitude_longitude():
    user = User.objects.create_user(username='testuser',
                                    password='testpassword',
                                    email='testuser@example.com')
    poi = PointOfInterest(
        user=user,
        description='Valid coordinates',
        latitude=45.0,
        longitude=90.0
    )
    poi.full_clean()  # This should not raise a ValidationError
    poi.save()
