# Generated by Django 5.1.7 on 2025-04-04 07:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('San_HNT', '0046_alter_order_stateorder'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='StateOrder',
            field=models.CharField(choices=[('Chờ xác nhận', 'ChoXacNhan'), ('Đã xác nhận', 'XacNhan'), ('Chờ giao hàng', 'ChoGiaoHang'), ('Hủy', 'Huy'), ('Đã hủy', 'DaHuy'), ('Đã giao', 'DaGiao')], default='ChoXacNhan', max_length=20),
        ),
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.CharField(choices=[('Cá nhân', 'Customer'), ('admin', 'Admin'), ('Nhân viên', 'Employee'), ('Tiểu thương hoặc danh nghiệp', 'Supplier')], default='Customer', max_length=50),
        ),
    ]
