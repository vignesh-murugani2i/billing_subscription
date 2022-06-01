from django.urls import path, include
from rest_framework.routers import DefaultRouter

from service.views import ServiceViewSet

router = DefaultRouter()
router.register('', ServiceViewSet, basename='service')
urlpatterns = router.urls
# urlpatterns = [
#     path('get_plans/<int:service_id>', v.items_not_done),
#     path('', include(router.urls)),
# ]

