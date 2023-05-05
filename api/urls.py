from rest_framework.routers import DefaultRouter

from api.views import ProfileViewSet, PatientViewSet


router = DefaultRouter()
router.register('profiles', ProfileViewSet)
router.register('patients', PatientViewSet)

urlpatterns = router.get_urls()