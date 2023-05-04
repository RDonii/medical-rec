from django.conf import settings
from model_bakery import baker
import pytest

from api.models import Profile


@pytest.mark.django_db
class TestCreateProfile:

    def test_autocreate_profile_for_new_user(self):
        user = baker.make(settings.AUTH_USER_MODEL)
        profile_exists = Profile.objects.filter(user_id=user.id).exists()

        assert profile_exists
