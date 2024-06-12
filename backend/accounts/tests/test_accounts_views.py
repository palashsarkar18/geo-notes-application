import pytest
from django.urls import reverse
from rest_framework import status
from accounts.models import User


@pytest.mark.django_db
def test_create_user_view(api_client):
    url = reverse('user-register')
    data = {
        'username': 'testuser',
        'password': 'testpassword',
        'email': 'testuser@example.com'
    }
    response = api_client.post(url, data, format='json')
    assert response.status_code == status.HTTP_201_CREATED
    assert User.objects.count() == 1
    assert User.objects.get().username == 'testuser'


@pytest.mark.django_db
def test_login_view(api_client):
    user = User.objects.create_user(
        username='testuser',
        password='testpassword',
        email='testuser@example.com'
    )
    api_client.force_authenticate(user=user)
    url = reverse('user-login')
    data = {
        'username': 'testuser',
        'password': 'testpassword'
    }
    response = api_client.post(url, data, format='json')
    print("I AM HERE")
    print(response)
    assert response.status_code == status.HTTP_200_OK
    assert 'token' in response.json()


@pytest.mark.django_db
def test_logout_view(api_client):
    user = User.objects.create_user(
        username='testuser',
        password='testpassword',
        email='testuser@example.com'
    )
    api_client.force_authenticate(user=user)
    url = reverse('user-logout')
    response = api_client.post(url)
    assert response.status_code == status.HTTP_200_OK
    assert response.json()['message'] == 'Logout successful'
