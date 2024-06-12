import pytest
from django.urls import reverse
from rest_framework import status
from accounts.models import User
from pois.models import PointOfInterest


@pytest.mark.django_db
def test_poi_list_create_view(api_client):
    user = User.objects.create_user(username='testuser',
                                    password='testpassword')
    api_client.force_authenticate(user=user)

    # Test creating a new POI
    url = reverse('poi-list-create')
    data = {
        "latitude": 60.1699,
        "longitude": 24.9384,
        "description": "Test POI"
    }
    response = api_client.post(url, data, format='json')
    assert response.status_code == status.HTTP_201_CREATED

    # Test listing POIs
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 1


@pytest.mark.django_db
def test_poi_detail_view(api_client):
    user = User.objects.create_user(username='testuser',
                                    password='testpassword')
    api_client.force_authenticate(user=user)
    poi = PointOfInterest.objects.create(
        user=user,
        latitude=60.1699,
        longitude=24.9384,
        description="Test POI"
    )

    # Test retrieving a POI
    url = reverse('poi-detail', args=[poi.id])
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert response.data['description'] == "Test POI"

    # Test updating a POI
    data = {"description": "Updated POI"}
    response = api_client.patch(url, data, format='json')
    assert response.status_code == status.HTTP_200_OK
    assert response.data['description'] == "Updated POI"

    # Test deleting a POI
    response = api_client.delete(url)
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert PointOfInterest.objects.count() == 0


@pytest.mark.django_db
def test_poi_list_create_view_with_mock(api_client, mocker):
    user = User.objects.create_user(username='testuser',
                                    password='testpassword')
    api_client.force_authenticate(user=user)

    mocker.patch('pois.models.PointOfInterest.objects.create',
                 return_value=PointOfInterest(
                     id=1,
                     user=user,
                     latitude=60.1699,
                     longitude=24.9384,
                     description="Mocked POI"))

    url = reverse('poi-list-create')
    data = {
        "latitude": 60.1699,
        "longitude": 24.9384,
        "description": "Test POI"
    }
    response = api_client.post(url, data, format='json')
    assert response.status_code == status.HTTP_201_CREATED
    assert response.data['description'] == "Mocked POI"
