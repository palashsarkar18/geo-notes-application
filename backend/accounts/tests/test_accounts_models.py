import pytest
from accounts.models import User


@pytest.mark.django_db
def test_user_creation():
    user = User.objects.create_user(
        username='testuser',
        password='testpassword',
        email='testuser@example.com'
    )
    assert user.username == 'testuser'
    assert user.email == 'testuser@example.com'
    assert user.check_password('testpassword')
