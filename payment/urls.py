from django.urls import path
from . import views
urlpatterns = [
    path('changeCartNumber', views.changeCartNumber, name='changeCartNumber'),
    path('changeCartNumber', views.changeCartNumber, name='changeCartNumber'),
    path('checkOrder', views.checkOrder, name='checkOrder'),
    path('getReport', views.getReport, name='getReport'),
]