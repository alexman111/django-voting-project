import pytest
from django.contrib.auth.models import User


@pytest.fixture
def user_factory(db):
    def create_user(username = 'TestUser', password = 'TestPassword', email = 'test@mail.ru'):
        if User.objects.filter(username=username).exists():
            return User.objects.filter(username=username).first()
        else:
            user = User.objects.create(username=username, password=password, email=email)
            return user

    return create_user()


def test_user_username(db, user_factory):
    user = user_factory(username='testUser')
    assert user.username == 'testUser'
