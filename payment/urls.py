from django.urls import path
from . import views
urlpatterns = [
    path('changeCartNumber', views.changeCartNumber, name='changeCartNumber'),
    path('changeCartNumber', views.changeCartNumber, name='changeCartNumber'),
    path('checkOrder', views.checkOrder, name='checkOrder'),
    path('getReport', views.getReport, name='getReport'),
    path('RegisterBuyRequest', views.RegisterBuyRequest, name='RegisterBuyRequest'),
    path('DeleteTransaction/<int:id>/<str:type>', views.DeleteTransaction, name='DeleteTransaction'),
    path('withdrawalCustomer', views.withdrawalCustomer, name='withdrawalCustomer'),
    path('changeGoldRequest/<str:rate>', views.changeGoldRequest, name='changeGoldRequest'),
    path('changeGoldToMoneyRequest/<str:rate>', views.changeGoldToMoneyRequest, name='changeGoldToMineyRequest'),
    path('getGoldRequest/', views.get_gold_request, name='getGoldRequest'),
]