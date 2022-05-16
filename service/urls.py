from rest_framework.routers import DefaultRouter

from service.views import ServiceViewSet

router = DefaultRouter()
router.register('', ServiceViewSet, basename='service')
urlpatterns = router.urls

