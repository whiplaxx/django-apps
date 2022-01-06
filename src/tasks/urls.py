from django.urls import path

from . import views

app_name = 'tasks'
urlpatterns = [
    path('', views.index, name='index'),
    path('save/', views.saveTask, name='save'),
    path('delete/', views.deleteTask, name='delete'),
    path('react/', views.react, name='react'),
]

