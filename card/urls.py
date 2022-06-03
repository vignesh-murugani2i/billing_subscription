from django.urls import path, include
from rest_framework.routers import DefaultRouter

#from card.views import CardView

# router = DefaultRouter()
# router.register('', CardView, basename='card')
# urlpatterns = router.urls
from card import views

urlpatterns = [
    path('card/', views.create_card),
    path('card/<int:card_id>', views.get_card_by_id),
    path('cards/', views.get_all_card),
    path('card/<int:card_id>/update', views.update_card_by_id),
    path('card/<int:card_id>/delete', views.delete_card_by_id),
]
