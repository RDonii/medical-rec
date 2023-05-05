from rest_framework import serializers

from api.models import Profile


class ProfileSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = ['id', 'full_name', 'company_name', 'birth_date', 'user_id']

    def get_full_name(self, profile: Profile) -> str:
        return profile.user.get_full_name()
