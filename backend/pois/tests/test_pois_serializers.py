import pytest
from accounts.models import User
from pois.serializers import PointOfInterestSerializer
from pois.models import PointOfInterest


@pytest.mark.django_db
def test_poi_serializer():
    user = User.objects.create_user(username='testuser',
                                    password='testpassword')
    poi = PointOfInterest.objects.create(
        user=user,
        latitude=60.1699,
        longitude=24.9384,
        description="Test POI"
    )
    serializer = PointOfInterestSerializer(poi)
    data = serializer.data
    assert data['latitude'] == "60.169900"
    assert data['longitude'] == "24.938400"
    assert data['description'] == "Test POI"
