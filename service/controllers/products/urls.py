from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='products_index'),
    path('search/', views.product_search, name='products_search'),
    path('details/<int:product_id>/', views.details, name='products_details'),
    path('details/data/<int:product_id>/', views.details_insights,
         name='products_details_data'),
    path('create/', views.create, name='products_create'),
    path('create/<int:product_id>', views.create, name='products_edit'),
    path('create/gallery/<int:product_id>/', views.add_gallery_image,
         name='products_add_img'),
    path('gallery/<int:product_id>/', views.gallery, name='products_gallery'),
    path('gallery/remove/',
         views.remove_gallery_image, name='products_remove_img'),
]
