# Generated by Django 5.1.7 on 2025-03-20 09:58

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('San_HNT', '0009_remove_category_supplier_supplier_categorys_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='Description',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='comment',
            name='Reply',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='San_HNT.comment'),
        ),
        migrations.AlterField(
            model_name='product',
            name='Description',
            field=models.TextField(blank=True, null=True),
        ),
    ]
