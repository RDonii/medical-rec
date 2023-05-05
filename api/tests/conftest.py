from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
import pytest

from api.models import Profile


@pytest.fixture
def client():
    return APIClient()

@pytest.fixture
def admin_user_data():
    return {
        "email": 'admin@example.com',
        "username": 'admin',
        "password": 'admin123',
    }

@pytest.fixture
def user_data():
    return {
        "email": 'user@example.com',
        "username": 'user',
        "password": 'user_password123',
    }

@pytest.fixture
def profile_data():
    return {
        "company_name": "Example Company",
        'birth_date': '1999-12-31'
    }

@pytest.fixture
def admin_user(admin_user_data):
    User = get_user_model()
    return User.objects.create_superuser(**admin_user_data)

@pytest.fixture
def user(user_data):
    User = get_user_model()
    return User.objects.create(**user_data)

@pytest.fixture
def admin_client(admin_user, client):
    client.force_authenticate(user=admin_user)
    return client

@pytest.fixture
def user_client(user, client):
    client.force_authenticate(user=user)
    return client
