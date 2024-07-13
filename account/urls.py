from django.urls import path
from . import views
urlpatterns = [
    path('', views.LoginRequest, name='login'),
    path('signin/', views.signin, name='index'),
    path('adminCustome/', views.admin, name='adminCustome'),
]