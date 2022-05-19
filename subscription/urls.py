from django.urls import path

from subscription import views

urlpatterns = [
    path('subscription/', views.create_subscription),
    path('subscriptions/', views.get_all_subscription, name='get_all_subscription'),
    path('subscription/<int:subscription_id>', views.get_subscription_by_id, name='get_subscription_by_id'),
    path('subscription/<int:subscription_id>/update', views.update_subscription_by_id, name='update_subscription_by_id'),
    path('subscription/<int:subscription_id>/delete', views.delete_subscription_by_id, name='delete_subscription_by_id'),
]