from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='admin_orders_index'),
    path('order/actions/', views.order_actions, name='order_actions'),
    path('order/process/', views.order_process, name='admin_order_process')
]
