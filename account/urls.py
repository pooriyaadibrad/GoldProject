from django.urls import path
from . import views
urlpatterns = [
    path('', views.Login, name='index'),
    path('signin/', views.signin, name='index'),
]