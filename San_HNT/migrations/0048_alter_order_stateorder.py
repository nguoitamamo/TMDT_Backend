# Generated by Django 5.1.7 on 2025-04-04 09:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('San_HNT', '0047_alter_order_stateorder_alter_user_role'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='StateOrder',
            field=models.CharField(choices=[('Chờ xác nhận', 'ChoXacNhan'), ('Đã xác nhận', 'XacNhan'), ('Chờ giao hàng', 'ChoGiaoHang'), ('Hủy', 'Huy'), ('Đã hủy', 'DaHuy'), ('Đã giao', 'DaGiao')], default='Chờ xác nhận', max_length=20),
        ),
    ]
