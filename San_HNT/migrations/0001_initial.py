# Generated by Django 5.1.7 on 2025-03-20 07:56

import cloudinary.models
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('NgayTao', models.DateTimeField(auto_now_add=True)),
                ('NgayUpdate', models.DateTimeField(auto_now=True)),
                ('Active', models.BooleanField(default=True)),
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('TenDangNhap', models.CharField(max_length=50, unique=True)),
                ('MatKhau', models.CharField(max_length=100)),
                ('Role', models.CharField(choices=[('customer', 'Customer'), ('admin', 'Admin'), ('employee', 'Employee'), ('supplier', 'Supplier')], default='customer', max_length=10)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('NgayTao', models.DateTimeField(auto_now_add=True)),
                ('NgayUpdate', models.DateTimeField(auto_now=True)),
                ('Active', models.BooleanField(default=True)),
                ('CategoryID', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('CategoryName', models.CharField(max_length=100)),
                ('Description', models.TextField()),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('NgayTao', models.DateTimeField(auto_now_add=True)),
                ('NgayUpdate', models.DateTimeField(auto_now=True)),
                ('Active', models.BooleanField(default=True)),
                ('OrderID', models.AutoField(primary_key=True, serialize=False)),
                ('TypePay', models.CharField(choices=[('tienmat', 'TienMat'), ('online', 'Online')], default='online', max_length=10)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('CustomerID', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='San_HNT.account')),
            ],
        ),
        migrations.CreateModel(
            name='Supplier',
            fields=[
                ('NgayTao', models.DateTimeField(auto_now_add=True)),
                ('NgayUpdate', models.DateTimeField(auto_now=True)),
                ('Active', models.BooleanField(default=True)),
                ('SupplierID', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='San_HNT.account')),
                ('TotalComment', models.IntegerField(default=0)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='UserInfo',
            fields=[
                ('account', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='San_HNT.account')),
                ('Ho', models.CharField(max_length=20)),
                ('Ten', models.CharField(max_length=20)),
                ('Image', cloudinary.models.CloudinaryField(max_length=255, null=True)),
                ('NgaySinh', models.DateField(null=True)),
                ('DiaChi', models.TextField(null=True)),
                ('Email', models.CharField(max_length=100, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('NgayTao', models.DateTimeField(auto_now_add=True)),
                ('NgayUpdate', models.DateTimeField(auto_now=True)),
                ('Active', models.BooleanField(default=True)),
                ('ProductID', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('ProductName', models.CharField(max_length=100)),
                ('UnitPrice', models.FloatField()),
                ('Description', models.TextField()),
                ('Category', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='products', to='San_HNT.category')),
                ('Supplier', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='products', to='San_HNT.supplier')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='OrderDetail',
            fields=[
                ('OrderDetailID', models.AutoField(primary_key=True, serialize=False)),
                ('Quantity', models.IntegerField()),
                ('UnitPrice', models.FloatField()),
                ('Discount', models.FloatField()),
                ('Order', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='order_details', to='San_HNT.order')),
                ('Product', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='order_details', to='San_HNT.product')),
            ],
        ),
        migrations.AddField(
            model_name='order',
            name='Customer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='orders', to='San_HNT.customer'),
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('NgayTao', models.DateTimeField(auto_now_add=True)),
                ('NgayUpdate', models.DateTimeField(auto_now=True)),
                ('Active', models.BooleanField(default=True)),
                ('CommentID', models.AutoField(primary_key=True, serialize=False)),
                ('Content', models.CharField(max_length=200)),
                ('IDEdComment', models.CharField(max_length=20)),
                ('Customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='San_HNT.customer')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
