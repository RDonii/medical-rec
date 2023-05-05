from rest_framework import serializers

from api.models import Material, Patient, Profile


class ProfileSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = ['id', 'full_name', 'company_name', 'birth_date', 'user_id']

    def get_full_name(self, profile: Profile) -> str:
        return profile.user.get_full_name()


class PatientSerializer(serializers.ModelSerializer):
    '''
    Serializer for non admin users.
    Links user.profile to doctor field on creation.
    '''

    class Meta:
        model = Patient
        fields = ['id', 'first_name', 'last_name', 'birth_date', 'gender', 'med_condition', 'created', 'updated',]

    def create(self, validated_data):
        user = self.context.get('request').user

        # Guard against incorrect use of serializer with admin users
        assert not user.is_staff, (
            f"You can not use {self.__class__.__name__} serializer with admin users."
        )

        return Patient.objects.create(doctor_id=user.profile.id, **validated_data)
    

class FullPatientSerializer(serializers.ModelSerializer):
    '''
    Serializer for admin get views.
    Renders profile object on doctor field
    '''

    doctor = ProfileSerializer(read_only=True)

    class Meta:
        model = Patient
        fields = ['id', 'first_name', 'last_name', 'birth_date', 'gender', 'med_condition', 'doctor', 'created', 'updated',]


class CreatePatientSerializer(serializers.ModelSerializer):
    '''
    Serializer for admin create/update views.
    Requires profile object for doctor field.
    '''

    class Meta:
        model = Patient
        fields = ['id', 'first_name', 'last_name', 'birth_date', 'gender', 'med_condition', 'doctor', 'created', 'updated',]


class MaterialSerializer(serializers.ModelSerializer):

    class Meta:
        model = Material
        fields = ['id', 'file', 'created', 'updated']
    
    def create(self, validated_data):
        patient_id = self.context.get('patient_id')
        return Material.objects.create(patient_id=patient_id, **validated_data)