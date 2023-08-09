
from django.urls import path,include
from . import views

urlpatterns = [
    # Examples:
    path('', views.home, name='home'),
    path('payment/<str:order_id>', views.payment, name='payment'),
    path('response/',views.response, name='response'),
]
