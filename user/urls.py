from django.urls import path, include

from user import views

urlpatterns = [
    path('user/', views.create_user, name='create'),
    path('users/', views.get_all_user, name='get_all_user'),
    path('user/<int:user_id>/', views.get_user_by_id, name='get_user_by_id'),
    path('user/<int:user_id>', views.update_user_by_id, name='update_user_by_id'),
    path('user/<int:user_id>/delete', views.delete_user_by_id, name='delete_user_by_id'),
]