from django.contrib.auth import get_user_model
from service.models import Tracking, Product, Order, UserRole, ProductGalleryImage
from service.database.repository import Repository


User = get_user_model()

products = Repository(Product)
product_images = Repository(ProductGalleryImage)
trackings = Repository(Tracking)
orders = Repository(Order)
users = Repository(User)
user_roles = Repository(UserRole)


class UnitOfWork():
    def __init__(self):
        self.products = products
        self.product_images = product_images
        self.trackings = trackings
        self.orders = orders
        self.users = users
        self.user_roles = user_roles
