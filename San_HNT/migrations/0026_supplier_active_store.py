# Generated by Django 5.1.7 on 2025-03-25 06:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('San_HNT', '0025_alter_product_productid'),
    ]

    operations = [
        migrations.AddField(
            model_name='supplier',
            name='Active_Store',
            field=models.BooleanField(default=False, null=True),
        ),
    ]
