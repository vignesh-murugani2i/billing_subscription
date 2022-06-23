from django.urls import path, include

from tenant import views

urlpatterns = [
    path('tenant/', views.create_tenant),
    path('tenants/', views.get_all_tenant),
    path('tenant/<int:tenant_id>/', views.get_tenant_by_id),
    path('tenant/<int:tenant_id>/update', views.update_tenant_by_id),
    path('tenant/<int:tenant_id>/delete', views.delete_tenant_by_id),
    path('tenant/users/<int:tenant_id>', views.get_all_user_by_tenant_id),
    path('tenant/subscriptions/<int:tenant_id>', views.get_all_subscriptions_by_tenant_id),
    path('tenant/payments/<int:tenant_id>', views.get_all_payments_by_tenant_id)
]
