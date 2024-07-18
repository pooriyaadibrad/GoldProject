from django.urls import path
from . import views
urlpatterns = [
    path('', views.LoginRequest, name='login'),
    path('signin/', views.signin, name='signin'),
    path('adminCustome/', views.admin, name='adminCustome'),
    path('logout/', views.Logout, name='logout'),
    path('activeCustomer/<int:id>', views.activeCustomer, name='activeCustomer'),
    path('DeleteCustomer/<int:id>', views.DeleteCustomer, name='DeleteCustomer'),
    path('BlockCustomer/<int:id>', views.BlockCustomer, name='BlockCustomer'),
]