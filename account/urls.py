from django.urls import path
from . import views
urlpatterns = [
    path('', views.Login, name='login'),
    path('LoginRequest/', views.LoginRequest, name='LoginRequest'),
    path('signin/', views.signin, name='index'),
    path('admin/', views.admin, name='admin'),
]