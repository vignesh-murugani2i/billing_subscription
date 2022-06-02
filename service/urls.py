from django.urls import path, include, re_path
from rest_framework.routers import DefaultRouter

from service import views
from service.views import ServiceViewSet

router = DefaultRouter()
router.register('', ServiceViewSet, basename='service')
# urlpatterns = router.urls
urlpatterns = [
    path('plans/<int:service_id>/', ServiceViewSet.as_view({"get": "get_plans_by_service_id"}),
         name="get_plans_by_service_id"),

]
