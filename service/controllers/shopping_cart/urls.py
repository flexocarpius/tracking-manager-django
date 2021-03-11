from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='shopping_cart_index'),
]
