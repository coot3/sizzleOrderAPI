from django.contrib import admin
from django.urls import path, include
from .views import ProductsAPI, CreateOrderAPI, CurrentOrdersAPI

urlpatterns = [
    path('products/', ProductsAPI.as_view()),
    path('create_order/', CreateOrderAPI.as_view()),
    path('current_orders/', CurrentOrdersAPI.as_view())
] 

