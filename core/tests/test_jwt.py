from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
import pytest


@pytest.fixture
def new_user_data():
    return {
        "username": "testusername",
        "password": "testpassword123"
    }

@pytest.fixture
def client():
    return APIClient()

@pytest.fixture
def new_user(new_user_data):
    # can not use baker when password must be hashed
    return get_user_model().objects.create_user(**new_user_data)


@pytest.mark.django_db
class TestJwtAuthentication:

    def test_login(self, client, new_user, new_user_data):
        response = client.post(reverse('jwt-create'), data=new_user_data)

        assert response.status_code == status.HTTP_200_OK

    def test_refresh(self, client, new_user, new_user_data):
        refresh_token  = client.post(reverse('jwt-create'), data=new_user_data).data['refresh']
        
        response = client.post(reverse('jwt-refresh'), data={
            "refresh": refresh_token
        })

        assert response.status_code == status.HTTP_200_OK
        assert 'access' in response.data.keys()

    def test_verify(self, client, new_user, new_user_data):
        access_token  = client.post(reverse('jwt-create'), data=new_user_data).data['access']
        
        response = client.post(reverse('jwt-verify'), data={
            "token": access_token
        })

        assert response.status_code == status.HTTP_200_OK