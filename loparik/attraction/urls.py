from django.urls import path

from . import views

app_name = 'attraction'

urlpatterns = [
    path('', views.index, name='index'),
    path('topic_pk:int/', views.topic, name='topic'),
    path('topic_pk:int/sub_topic_pk:int/', views.subtopic, name='subtopic')  
]