# Generated by Django 5.1.7 on 2025-03-27 18:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('San_HNT', '0031_alter_orderdetail_unitprice_alter_product_unitprice'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='UnitPrice',
            field=models.CharField(max_length=20, null=True),
        ),
    ]
