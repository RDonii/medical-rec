from django.conf import settings
from django.urls import reverse
from rest_framework import status
from model_bakery import baker
import pytest

from api.models import Profile
from api.serializers import ProfileSerializer


@pytest.mark.django_db
class TestCreateProfile:

    def test_autocreate_profile_for_new_user(self):
        user = baker.make(settings.AUTH_USER_MODEL)
        profile_exists = Profile.objects.filter(user_id=user.id).exists()

        assert profile_exists


@pytest.mark.django_db
class TestListProfile:
    url = reverse('profile-list')

    def test_if_user_anonymous_returns_401(self, client):
        response = client.get(self.url)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_user_not_admin_returns_403(self, user_client):
        response = user_client.get(self.url)

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_get_profiles_if_admin(self, admin_client):

        response = admin_client.get(self.url)

        assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
class TestRetrieveProfile:
    url = reverse('profile-me')

    def test_retrieve_profile_me(self, user_client, user):
        response = user_client.get(self.url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data == ProfileSerializer(user.profile).data

    def test_if_user_anonymous_returns_401(self, client):
        response = client.get(self.url)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
class TestUpdateProfile:
    url = reverse('profile-me')

    def test_if_user_anonymous_returns_401(self, client):
        response = client.patch(self.url, data={})

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_partial_change_profile(self, user_client, user, profile_data):
        old_birth_date = str(user.profile.birth_date)

        response = user_client.patch(self.url, data={
            'company_name': profile_data['company_name']
        })
        user.profile.refresh_from_db()

        assert response.status_code == status.HTTP_200_OK
        assert user.profile.company_name == profile_data['company_name']
        assert str(user.profile.birth_date) == old_birth_date
