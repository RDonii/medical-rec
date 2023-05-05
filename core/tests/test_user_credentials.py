from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
import pytest


@pytest.fixture
def new_user(new_user_data):
    # can not use baker when password must be hashed
    return get_user_model().objects.create_user(**new_user_data)

@pytest.fixture
def authenticated_client(client, new_user):
    client.force_authenticate(user=new_user)
    return client


@pytest.mark.django_db
class TestUserPassword:

    def test_set_new_password(self, authenticated_client, new_user, new_user_data):
        new_password = 'new_password_951753'

        response = authenticated_client.post(reverse('user-set-password'), data={
            "new_password": new_password,
            "current_password": new_user_data["password"]
        })

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert new_user.check_password(new_password)

    def test_set_new_password_with_invalid_current_password(self, authenticated_client):
        new_password = 'new_password_951753'

        response = authenticated_client.post(reverse('user-set-password'), data={
            "new_password": new_password,
            "current_password": 'invalid_password_95175'
        })

        assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
class TestUserUsername:

    def test_set_new_username(self, authenticated_client, new_user, new_user_data):
        new_username = "new_username"

        response = authenticated_client.post(reverse('user-set-username'), data={
            "new_username": new_username,
            "current_password": new_user_data["password"]
        })
        new_user.refresh_from_db()

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert new_user.get_username() == new_username
    
    def test_set_new_username_with_invalid_current_password(self, authenticated_client):
        new_username = "new_username"

        response = authenticated_client.post(reverse('user-set-username'), data={
            "new_username": new_username,
            "current_password": 'invalid_password_95175'
        })

        assert response.status_code == status.HTTP_400_BAD_REQUEST
