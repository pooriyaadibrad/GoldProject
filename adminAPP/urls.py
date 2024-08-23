from django.urls import path
from . import views
urlpatterns = [
    path('', views.admin, name='adminAPP'),
    path('cartNumber/', views.cartNumber, name='cartNumber'),
    path('changeToGold/', views.changeToGold, name='changeToGold'),
    path('report/', views.report, name='report'),
    path('requestCustomer/', views.requestCustomer, name='requestCustomer'),
    path('settlement/', views.settlement, name='settlement'),
    path('userInfo/', views.userInfo, name='userInfo'),
    path('withdrawal/', views.withdrawal, name='withdrawal'),
    path('DeterminingGoldPrice/', views.DeterminingGoldPrice, name='DeterminingGoldPrice'),
    path('ConvertMoneyRequest/', views.ConvertMoneyRequest, name='ConvertMoneyRequest'),
    path('GetGoldRequest/', views.GetGoldRequest, name='GetGoldRequest'),
]