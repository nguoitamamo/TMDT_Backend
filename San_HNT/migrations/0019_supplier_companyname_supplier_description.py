# Generated by Django 5.1.7 on 2025-03-23 11:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('San_HNT', '0018_alter_user_role'),
    ]

    operations = [
        migrations.AddField(
            model_name='supplier',
            name='CompanyName',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='supplier',
            name='Description',
            field=models.TextField(blank=True, null=True),
        ),
    ]
