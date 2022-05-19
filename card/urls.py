from django.urls import path, include
from rest_framework.routers import DefaultRouter

#from card.views import CardView

# router = DefaultRouter()
# router.register('', CardView, basename='card')
# urlpatterns = router.urls
from card import views

urlpatterns = [
    path('card/', views.create_card),
]
