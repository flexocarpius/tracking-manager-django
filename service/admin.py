from django.contrib import admin

# Register your models here.
from .models import Tracking, Product, Order

admin.site.register(Tracking)
admin.site.register(Product)
admin.site.register(Order)
