# Generated by Django 5.1.7 on 2025-03-23 05:38

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('San_HNT', '0015_order_stateorder_deals_dealproducts'),
    ]

    operations = [
        migrations.AddField(
            model_name='deals',
            name='CategoryID',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='San_HNT.category'),
        ),
        migrations.DeleteModel(
            name='DealProducts',
        ),
    ]
