from django.urls import path
from . import views

app_name = 'service'
urlpatterns = [
    path('', views.index, name='index'),
    path('week_earnings/', views.week_earnings_day, name='week_earnings'),
    path('total_progress/', views.total_progress, name='total_progress'),
    path('featured_products/', views.get_featured_products,
         name='featured_products'),
    path('orders_state/', views.orders_state,
         name='orders_state'),
]
