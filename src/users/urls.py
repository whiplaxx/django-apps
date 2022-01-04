from django.urls import path
from . import views

app_name = 'users'
urlpatterns = [
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.logoutView, name='logout'),
    path('signup/', views.signup, name='signup'),
    path('profile/', views.profile, name='profile')
]

