import pytest
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
from simpleblog.tests.factories import BaseUserFactory, PostFactory, ContactFactory

@pytest.fixture
def api_client():
    user = User.objects.create_user(username= 'testuser', password='Jalal123!@#',email='testuser@gmail.com', first_name = None, last_name = None)
    client = APIClient()
    refresh = RefreshToken.for_user(user)
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')

    return client 

@pytest.fixture
def user1():
    return BaseUserFactory()

@pytest.fixture
def user2():
    return BaseUserFactory()

@pytest.fixture
def post1(user1):
    return PostFactory(author=user1)

@pytest.fixture
def contact1():
    return ContactFactory()
