from rest_framework.routers import DefaultRouter

from card.views import CardView

router = DefaultRouter()
router.register('', CardView, basename='card')
urlpatterns = router.urls
