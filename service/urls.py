"""
Default urls
"""
from django.urls import path, include

urlpatterns = [
    path('', include('service.controllers.home.urls')),
    path('trackings/', include('service.controllers.trackings.urls')),
    path('products/', include('service.controllers.products.urls')),
    path('users/', include('service.controllers.users.urls')),
    path('orders/', include('service.controllers.orders.urls')),
    path('account/', include('service.controllers.account.urls')),
    path('shopping_cart/', include('service.controllers.shopping_cart.urls')),
    path('admin_orders/', include('service.controllers.admin_orders.urls')),
    path('dashboard/', include('service.controllers.dashboard.urls', namespace='dashboard'))
]
