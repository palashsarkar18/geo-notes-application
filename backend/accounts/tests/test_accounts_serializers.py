import pytest
from accounts.models import User
from accounts.serializers import UserSerializer


@pytest.mark.django_db
def test_user_serializer():
    user = User.objects.create_user(
        username='testuser',
        password='testpassword',
        email='testuser@example.com'
    )
    serializer = UserSerializer(user)
    data = serializer.data
    assert data['username'] == 'testuser'
    assert data['email'] == 'testuser@example.com'

    # Test the create method of the serializer
    new_user_data = {
        'username': 'newuser',
        'password': 'newpassword',
        'email': 'newuser@example.com'
    }
    serializer = UserSerializer(data=new_user_data)
    assert serializer.is_valid()
    new_user = serializer.save()
    assert new_user.username == 'newuser'
    assert new_user.email == 'newuser@example.com'
    assert new_user.check_password('newpassword')
