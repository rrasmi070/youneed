from django.contrib import admin
from .models import Category,Product,Cart,Cartproduct,Order,Moreimage
# Register your models here.

# admin.site.register(Carousel)
admin.site.register(Product)
admin.site.register(Category)
admin.site.register(Cart)
admin.site.register(Cartproduct)
admin.site.register(Order)
admin.site.register(Moreimage)