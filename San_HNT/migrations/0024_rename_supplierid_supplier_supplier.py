# Generated by Django 5.1.7 on 2025-03-24 05:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('San_HNT', '0023_remove_supplier_avatar'),
    ]

    operations = [
        migrations.RenameField(
            model_name='supplier',
            old_name='SupplierID',
            new_name='Supplier',
        ),
    ]
