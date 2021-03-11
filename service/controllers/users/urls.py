from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='users_index'),
    path('register/', views.register, name='users_register'),
    path('register/<user_id>/', views.register, name='users_register')
]
