# Generated by Django 5.1.7 on 2025-03-29 06:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('San_HNT', '0035_alter_productimage_image_alter_user_avatar'),
    ]

    operations = [
        migrations.RenameField(
            model_name='customer',
            old_name='CustomerID',
            new_name='Customer',
        ),
    ]
