from django.urls import path, include

from payment import views

urlpatterns = [
    path('payment/', views.make_all_subscriptions_payment,),

]
