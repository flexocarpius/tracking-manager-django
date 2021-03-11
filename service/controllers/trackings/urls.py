from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='trackings_index'),
    path('details/<int:tracking_id>', views.details, name='trackings_details'),
    # API calls
    path('order/<int:order_id>', views.trackings_order, name='trackings_order'),
    path('process/', views.trackings_process, name='trackings_process'),
]
