from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import ListModelMixin, UpdateModelMixin
from rest_framework.permissions import IsAdminUser, IsAuthenticated

from api.models import Profile
from api.serializers import ProfileSerializer


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