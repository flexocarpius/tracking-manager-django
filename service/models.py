"""models.py
Contain all the models from the service application.
"""
from django.db import models
from django.contrib.auth.models import User
import random


class Product(models.Model):
    """Product
    Describes a product inside the application.
    """
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=5000)
    price = models.FloatField()
    quantity = models.IntegerField()
    small_img = models.CharField(max_length=500, blank=True, null=True)
    large_img = models.CharField(max_length=500, blank=True, null=True)

    def to_dict(self):
        return {
            'id': self.pk,
            'name': self.name,
            'description': self.description,
            'price': self.price,
            'quantity': self.quantity,
            'small_img': self.small_img,
            'large_img': self.large_img,
        }


class ProductGalleryImage(models.Model):
    """ProductGalleryImage
    Contains the gallery of images of one product.
    """
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    img_url = models.CharField(max_length=500)

    def to_dict(self):
        return {
            'id': self.pk,
            'product': self.product.to_dict(),
            'img_url': self.img_url
        }


class Order(models.Model):
    """Order
    Haves a list of trackings, describing the contents of it.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    code = models.CharField(max_length=50, blank=True, null=True)
    shipping_address = models.CharField(max_length=500, blank=True, null=True)
    state = models.CharField(max_length=100)
    payment_reference = models.CharField(max_length=100, blank=True, null=True)
    payment_date = models.DateField(blank=True, null=True)
    total = models.FloatField(blank=True, null=True)
    created_date = models.DateField(blank=True, null=True)
    placed_date = models.DateField(blank=True, null=True)
    cancelled_date = models.DateField(blank=True, null=True)
    refunded_date = models.DateField(blank=True, null=True)

    def to_dict(self):
        return {
            'id': self.pk,
            'user': self.user,
            'code': self.code,
            'shipping_address': self.shipping_address,
            'state': self.state,
            'payment_reference': self.payment_reference,
            'payment_date': self.payment_date,
            'total': self.total,
            'created_date': self.created_date,
            'placed_date': self.placed_date,
            'cancelled_date': self.cancelled_date,
            'refunded_date': self.refunded_date
        }

    def save(self, *args, **kwargs):
        if (self.total is not None):
            self.total = float('{0:10.2f}'.format(self.total))
        super(Order, self).save(*args, **kwargs)

    @classmethod
    def generate_code(cls, order_id):
        char_codes = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        number_codes = '0123456789'
        return '{0}{1}{2}{3}'.format(''.join(random.sample(char_codes, 5)), ''.join(random.sample(number_codes, 3)), ''.join(random.sample(char_codes, 3)), order_id)


class Tracking(models.Model):
    """Tracking
    Gets a detail of an order, this is called a Tracking.
    """
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=500)
    state = models.CharField(max_length=100)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    shipping_code = models.CharField(max_length=100, blank=True, null=True)
    shipped_date = models.DateField(blank=True, null=True)
    delivered_date = models.DateField(blank=True, null=True)
    cancelled_date = models.DateField(blank=True, null=True)
    created_date = models.DateField(blank=True, null=True)
    placed_date = models.DateField(blank=True, null=True)
    delayed_date = models.DateField(blank=True, null=True)

    def to_dict(self):
        return {
            'id': self.pk,
            'name': self.name,
            'description': self.description,
            'state': self.state,
            'quantity': self.quantity,
            'product': self.product.to_dict(),
            'shipped_date': self.shipped_date,
            'delivered_date': self.delivered_date,
            'cancelled_date': self.cancelled_date,
            'created_date': self.created_date,
            'placed_date': self.placed_date,
            'delayed_date': self.delayed_date,
        }

    @classmethod
    def generate_code(cls, product_id):
        char_codes = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        number_codes = '0123456789'
        return '{0}{1}{2}{3}'.format(''.join(random.sample(char_codes, 5)), ''.join(random.sample(number_codes, 3)), ''.join(random.sample(char_codes, 3)), product_id)


class UserRole(models.Model):
    """User
    Describes an user in the system, apart from the Django users
    """
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True
    )
    state = models.CharField(max_length=100)
    role = models.CharField(max_length=100)
