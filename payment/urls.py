from django.urls import path, include

from payment import views

urlpatterns = [
    path('all_payments/', views.make_all_subscriptions_payment,),
    path('payment/<int:payment_id>', views.get_payment_by_id,),
    path('payments/', views.get_all_payments,),

]
