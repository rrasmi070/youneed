# Generated by Django 3.1.5 on 2021-02-09 17:53

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total', models.PositiveIntegerField(default=0)),
                ('customer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category_name', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Product_name', models.CharField(max_length=20)),
                ('Price', models.FloatField()),
                ('brand', models.CharField(max_length=30)),
                ('Description', models.TextField()),
                ('image', models.FileField(upload_to='product/')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ecomm.category')),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_by', models.CharField(max_length=250)),
                ('shiping_address', models.TextField()),
                ('mobile', models.CharField(max_length=12)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('subtotal', models.PositiveIntegerField()),
                ('discount', models.PositiveIntegerField()),
                ('total', models.PositiveIntegerField()),
                ('order_status', models.CharField(blank=True, choices=[('Order Placed', 'Order Placed'), ('Payment Failed', 'Payment Failed'), ('Order Confirm', 'Order Confirm'), ('Order received', 'Order received'), ('Order Processing', 'Order Processing'), ('Order On The Way', 'Order On The Way'), ('Order Conpleated', 'Order Conpleated'), ('Order Canceled', 'Order Canceled')], max_length=50)),
                ('cresated_at', models.DateTimeField(auto_now_add=True)),
                ('pin_code', models.IntegerField()),
                ('payment_method', models.CharField(choices=[('Cash On DeliVery', 'Cash On DeliVery'), ('Make Payment', 'Make Payment')], default='Cash on DeliVery', max_length=30)),
                ('payment_status', models.BooleanField(blank=True, default=False, null=True)),
                ('razorpay_payment_id', models.CharField(blank=True, max_length=100)),
                ('razorpay_order_id', models.CharField(blank=True, max_length=100)),
                ('razorpay_signature', models.CharField(blank=True, max_length=100)),
                ('cart', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='ecomm.cart')),
            ],
        ),
        migrations.CreateModel(
            name='Moreimage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.FileField(upload_to='product/images/')),
                ('products', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ecomm.product')),
            ],
        ),
        migrations.CreateModel(
            name='Cartproduct',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rate', models.PositiveIntegerField()),
                ('quantity', models.PositiveIntegerField()),
                ('subtotal', models.PositiveIntegerField()),
                ('cart', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ecomm.cart')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ecomm.product')),
            ],
        ),
    ]
