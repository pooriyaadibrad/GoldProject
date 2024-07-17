from django.urls import path
from . import views
urlpatterns = [
    path('cartNumber/', views.cartNumber, name='payment'),
    path('changeToGold/', views.changeToGold, name='payment'),
]