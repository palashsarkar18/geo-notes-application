import pytest
from django.urls import reverse
from rest_framework import status
from accounts.models import User
from pois.models import PointOfInterest


@pytest.mark.django_db
def test_poi_update_delete_view(api_client):
    user1 = User.objects.create_user(username='user1', password='pass')
    user2 = User.objects.create_user(username='user2', password='pass')
    poi1 = PointOfInterest.objects.create(user=user1, latitude=60.1699,
                                          longitude=24.9384,
                                          description="POI 1")
    poi2 = PointOfInterest.objects.create(user=user2, latitude=61.1699,
                                          longitude=25.9384,
                                          description="POI 2")

    api_client.force_authenticate(user=user1)

    # Test updating own POI
    url = reverse('poi-detail', args=[poi1.id])
    data = {"description": "Updated POI 1"}
    response = api_client.patch(url, data, format='json')
    assert response.status_code == status.HTTP_200_OK
    assert response.data['description'] == "Updated POI 1"

    # Test updating another user's POI
    url = reverse('poi-detail', args=[poi2.id])
    data = {"description": "Updated POI 2"}
    response = api_client.patch(url, data, format='json')
    assert response.status_code == status.HTTP_403_FORBIDDEN

    # Test deleting own POI
    url = reverse('poi-detail', args=[poi1.id])
    response = api_client.delete(url)
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert PointOfInterest.objects.filter(id=poi1.id).count() == 0

    # Test deleting another user's POI
    url = reverse('poi-detail', args=[poi2.id])
    response = api_client.delete(url)
    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert PointOfInterest.objects.filter(id=poi2.id).count() == 1
