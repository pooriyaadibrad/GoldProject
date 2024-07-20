from django.urls import path
from . import views
urlpatterns = [
    path('', views.customer, name='customerAPP'),
    path('profile/', views.profile, name='profile'),
    path('withdrawalCustomer/', views.withdrawalCustomer, name='withdrawalCustomer'),
    path('settelment/', views.settelmentCustomer, name='settelmentCustomer'),
    path('ChangeGoldCustomer/',views.ChangeGoldCustomer,name='ChangeGoldCustomer'),
    path('reportCustomer/',views.reportCustomer,name='reportCustomer'),
]