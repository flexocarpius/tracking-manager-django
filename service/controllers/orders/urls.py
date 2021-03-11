from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='orders_index'),
    path('create/', views.create, name='orders_create'),
    path('cancel/', views.cancel_order, name='orders_cancel'),
    path('request_refund/', views.request_order_refund,
         name='orders_request_refund'),
    path('details/<int:order_id>', views.details, name='orders_details'),
    path('product/', views.add_product, name='orders_add_product'),
    path('product/remove', views.remove_product, name='orders_remove_product'),
    path('products/', views.get_products, name='orders_get_products'),
    path('actions/', views.order_actions, name='orders_actions'),
    path('place/', views.place_order, name='orders_place'),
    path('result/', views.order_placed, name='orders_result'),
    path('process/', views.set_order_placed, name='orders_set_placed'),
    path('product_details/<int:product_id>', views.product_details,
         name='orders_product_details'),
]
