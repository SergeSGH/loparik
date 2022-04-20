from django.urls import path

from . import views

app_name = 'attraction'

urlpatterns = [
    path('', views.index, name='index'),
    path('prizy/', views.prizy, name='prizy'),
    path('consult/', views.consult, name='consult')  
]
