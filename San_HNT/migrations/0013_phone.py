# Generated by Django 5.1.7 on 2025-03-22 06:25

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('San_HNT', '0012_user_address_user_avatar'),
    ]

    operations = [
        migrations.CreateModel(
            name='phone',
            fields=[
                ('phoneID', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('number', models.CharField(max_length=11)),
            ],
        ),
    ]
