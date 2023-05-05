from rest_framework import serializers

from api.models import Profile


class ProfileSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(read_only=True)

    class Meta:
        model = Profile
        fields = ['id', 'company_name', 'birth_date', 'user_id']