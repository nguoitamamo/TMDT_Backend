# Generated by Django 5.1.7 on 2025-03-29 06:18

import cloudinary.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('San_HNT', '0034_alter_productimage_image_alter_user_avatar'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productimage',
            name='image',
            field=cloudinary.models.CloudinaryField(max_length=255, null=True, verbose_name='Image'),
        ),
        migrations.AlterField(
            model_name='user',
            name='avatar',
            field=cloudinary.models.CloudinaryField(blank=True, max_length=255, null=True, verbose_name='avatar'),
        ),
    ]
