from django.urls import path

from . import views

app_name = 'orders'

urlpatterns = [
    path('order_create/', views.order_create, name='order_create'),
    path('order_create_success/', views.order_create_success, name='order_create_success'),
]
