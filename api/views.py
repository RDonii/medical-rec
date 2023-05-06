from typing import Union, Any
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.decorators import action
from rest_framework import status
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from rest_framework.mixins import ListModelMixin, UpdateModelMixin
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.permissions import SAFE_METHODS
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend

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
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['birth_date']
    search_fields = ['first_name', 'last_name', 'med_condition']
    ordering_fields = ['birth_date', 'created_at']

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
        self.queryset = self.queryset.filter(patient_id=self.kwargs["patient_pk"])
        if not user.is_staff:
            self.queryset = self.queryset.filter(patient__doctor_id=user.profile.id)
        return super().get_queryset()
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['patient_id'] = self.kwargs.get('patient_pk')
        return context

    def list(self, request, *args, **kwargs):
        patient_404 = self.has_parent_patient(request, kwargs['patient_pk'])
        if patient_404:
            return patient_404

        return super().list(request, *args, **kwargs)
    
    def create(self, request, *args, **kwargs):
        patient_404 = self.has_parent_patient(request, kwargs['patient_pk'])
        if patient_404:
            return patient_404

        return super().create(request, *args, **kwargs)

    def has_parent_patient(self, request: Request, patient_pk: Any) -> Union[Response, None]:
        '''
        Returns 404 response object if parent patient object does not exist or 
        parent patient object is not relative for non admin user
        '''
        if request.user.is_staff:
            patient = Patient.objects.filter(id=patient_pk)
        else:
            patient = Patient.objects.filter(id=patient_pk, doctor=request.user.profile)

        if not patient.exists():
            return Response(
                {'detail': 'Patient not found'},
                status=status.HTTP_404_NOT_FOUND
            )
