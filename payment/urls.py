from django.urls import path
from . import views
urlpatterns = [
    path('changeCartNumber', views.changeCartNumber, name='changeCartNumber'),
]