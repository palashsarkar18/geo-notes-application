import pytest
from pois.models import PointOfInterest
from accounts.models import User


@pytest.mark.django_db
def test_poi_creation():
    user = User.objects.create_user(username='testuser',
                                    password='testpassword')
    poi = PointOfInterest.objects.create(
        user=user,
        latitude=60.1699,
        longitude=24.9384,
        description="Test POI"
    )
    assert poi.user == user
    assert poi.latitude == 60.1699
    assert poi.longitude == 24.9384
    assert poi.description == "Test POI"
