from django.conf import settings
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from model_bakery import baker
import pytest


@pytest.fixture
def client():
    return APIClient()

@pytest.fixture
def new_user_data():
    return {
        "username": "testusername",
        "password": "testpassword123"
    }

@pytest.fixture
def new_user(new_user_data):
    return baker.make(settings.AUTH_USER_MODEL, **new_user_data)

@pytest.fixture
def new_staff_user(new_user_data):
    return baker.make(settings.AUTH_USER_MODEL, **new_user_data, is_staff=True)

@pytest.fixture
def authenticated_client(client, new_user):
    client.force_authenticate(new_user)
    return client

@pytest.fixture
def authenticated_staff_client(client, new_staff_user):
    client.force_authenticate(new_staff_user)
    return client


@pytest.mark.django_db
class TestCreateUser:
    
    def test_successful_user_registration_201(self, client, new_user_data):
        response = client.post(reverse('user-list'), new_user_data)

        assert response.data['id'] > 0
        assert "password" not in response.data.keys()
        assert response.status_code == status.HTTP_201_CREATED

    def test_not_unique_username_registration_400(self, client):
        user1 = baker.make(settings.AUTH_USER_MODEL)
        user_data = {
            "username": user1.username,
            "password": "38p&dsjk1355*"
        }

        response = client.post(reverse('user-list'), user_data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'username' in response.data.keys()


@pytest.mark.django_db
class TestRetrieveUser:

    def test_if_user_is_anonymous_returns_401(self, client):
        response = client.get(reverse('user-me'))

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_successful_retrieve_me(self, client):
        user = baker.make(settings.AUTH_USER_MODEL)
        client.force_authenticate(user=user)

        response = client.get(reverse('user-me'))

        assert response.status_code == status.HTTP_200_OK
        assert response.data["id"] == user.id

    def test_if_differant_id_returns_404(self, client):
        user = baker.make(settings.AUTH_USER_MODEL)
        client.force_authenticate(user=user)

        response = client.get(reverse('user-detail', args=[user.id+1]))

        assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
class TestListUser:

    def test_if_user_is_anonymous_returns_401(self, client):
        response = client.get(reverse('user-list'))

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
    
    def test_if_user_is_not_staff_returns_self(self, authenticated_client):
        response = authenticated_client.get(reverse('user-list'))

        assert response.status_code == status.HTTP_200_OK
        assert isinstance(response.data, list)
        assert len(response.data) == 1

    def test_if_user_is_staff_returns_all_users(self, authenticated_staff_client):
        baker.make(settings.AUTH_USER_MODEL, __quantity=8)

        response = authenticated_staff_client.get(reverse('user-list'))

        assert response.status_code == status.HTTP_200_OK
        assert isinstance(response.data, list)
        assert len(response.data) == get_user_model().objects.count()
