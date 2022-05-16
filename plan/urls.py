from rest_framework.routers import DefaultRouter

from plan.views import PlanViewSet

router = DefaultRouter()
router.register('', PlanViewSet, basename='plan')
urlpatterns = router.urls
