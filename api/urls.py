from rest_framework.routers import DefaultRouter
from rest_framework_nested.routers import NestedDefaultRouter

from api.views import ProfileViewSet, PatientViewSet, MaterialViewSet


router = DefaultRouter()
router.register('profiles', ProfileViewSet)
router.register('patients', PatientViewSet)

patient_router = NestedDefaultRouter(router, 'patients', lookup='patient')
patient_router.register('materials', MaterialViewSet)

urlpatterns = router.urls + patient_router.urls