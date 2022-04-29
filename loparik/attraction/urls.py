from django.urls import path

from . import views

app_name = 'attraction'

urlpatterns = [
    path('', views.index, name='index'),
    path('<slug:topic_slug>/', views.topic, name='topic'),
    path('<slug:topic_slug>/<slug:subtopic_slug>/', views.subtopic, name='subtopic')  
]
