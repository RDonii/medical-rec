from rest_framework.routers import DefaultRouter

from api.views import ProfileViewSet


router = DefaultRouter()
router.register('profiles', ProfileViewSet)

urlpatterns = router.get_urls()