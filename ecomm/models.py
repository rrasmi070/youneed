from django.db import models
from django.contrib.auth.models import User, auth


# Create your models here.
class Category(models.Model):
    category_name = models.CharField(max_length=30)

    def __str__(self):
        return self.category_name


class Product(models.Model):
    Product_name = models.CharField(max_length=20)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    Price = models.FloatField()
    brand = models.CharField(max_length=30)
    Description = models.TextField()
    image = models.FileField(upload_to="product/", max_length=None)

    def __str__(self):
        return self.Product_name

class Moreimage(models.Model):
    products = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = models.FileField(upload_to="product/images/",max_length=None)

    def __str__(self):
        return self.products.Product_name

    

class Cart(models.Model):
    customer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    total= models.PositiveIntegerField(default=0)
    def __str__(self):
        return "Cart: " +str(self.id)

class Cartproduct(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    rate = models.PositiveIntegerField()
    quantity = models.PositiveIntegerField()
    subtotal = models.PositiveIntegerField()
    def __str__(self):
        return "Cart: " +str(self.cart.id)+ "Cartproduct: " +str(self.id)

ORDER_STATUS = (
    ("Order Placed", "Order Placed"),
    ("Payment Failed", "Payment Failed"),
    ("Order Confirm", "Order Confirm"),
    ("Order received", "Order received"),
    ("Order Processing", "Order Processing"),
    ("Order On The Way", "Order On The Way"),
    ("Order Conpleated", "Order Conpleated"),
    ("Order Canceled", "Order Canceled"),
)

PAYMENT_METHOD = (
    ("Cash On DeliVery", "Cash On DeliVery"),
    ("Make Payment", "Make Payment"),
)

class Order(models.Model):
    cart = models.OneToOneField(Cart, on_delete=models.CASCADE)
    order_by = models.CharField(max_length=250)
    shiping_address = models.TextField()
    mobile = models.CharField(max_length=12)
    email = models.EmailField(null= True, blank=True)
    subtotal = models.PositiveIntegerField()
    discount = models.PositiveIntegerField()
    total = models.PositiveIntegerField()
    order_status = models.CharField(max_length=50, blank=True, choices=ORDER_STATUS)
    cresated_at = models.DateTimeField(auto_now_add=True)
    pin_code = models.IntegerField()
    payment_method = models.CharField(max_length=30, choices=PAYMENT_METHOD, default="Cash on DeliVery")
    payment_status = models.BooleanField(default=False, null=True, blank=True)
    razorpay_payment_id = models.CharField(max_length=100, blank=True)
    razorpay_order_id = models.CharField(max_length=100, blank=True)
    razorpay_signature = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return "Order:" +str(self.id)



# SEllER MODEL======================================================
# class Sell_reg(models.Model):
#     f_name =models.CharField(max_length=20)
#     l_name =models.CharField(max_length=20)
#     email =models.EmailField()
#     Phone =models.IntegerField()
#     dob =models.DateField()
#     IDproff =models.FileField(upload_to="id/")
#     IDproff =models.FileField(upload_to="id/")
