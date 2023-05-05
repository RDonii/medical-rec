from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from rest_framework.mixins import ListModelMixin, UpdateModelMixin
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.permissions import SAFE_METHODS

from api.models import Material, Patient, Profile
from api.serializers import (
    CreatePatientSerializer,
    FullPatientSerializer,
    PatientSerializer,
    ProfileSerializer,
    MaterialSerializer,
)


class ProfileViewSet(ListModelMixin, UpdateModelMixin, GenericViewSet):
    queryset = Profile.objects.select_related('user').all()
    serializer_class = ProfileSerializer
    permission_classes = [IsAdminUser]

    @action(detail=False, methods=['GET'], permission_classes=[IsAuthenticated], url_path='me', url_name='me')
    def get_profile(self, request):
        serializer = self.get_serializer(request.user.profile)
        return Response(serializer.data)

    @get_profile.mapping.patch
    def change_profile(self, request):
        serializer = self.get_serializer(request.user.profile, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class PatientViewSet(ModelViewSet):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if not user.is_staff:
            self.queryset = self.queryset.filter(doctor_id=user.profile.id)
        elif user.is_staff:
            self.queryset = self.queryset.select_related('doctor', 'doctor__user')
        return super().get_queryset()
    
    def get_serializer_class(self):
        if self.request.user.is_staff:
            if self.request.method in SAFE_METHODS:
                self.serializer_class = FullPatientSerializer
            else:
                self.serializer_class = CreatePatientSerializer
        return super().get_serializer_class()


class MaterialViewSet(ModelViewSet):
    queryset = Material.objects.all()
    serializer_class = MaterialSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if not user.is_staff:
            self.queryset = self.queryset.filter(patient__doctor_id=user.profile.id)
        return super().get_queryset()
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['patient_id'] = self.kwargs.get('patient_pk')
        return context