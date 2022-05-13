from django.urls import path, include

from tenant import views

urlpatterns = [
    path('tenant/', views.create_tenant),
    path('tenant/<int:tenant_id>', views.get_tenant_by_id)
]
