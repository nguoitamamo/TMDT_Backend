# Generated by Django 5.1.7 on 2025-03-23 06:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('San_HNT', '0017_alter_productimage_image_alter_user_avatar'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.CharField(choices=[('Cá nhân', 'Customer'), ('admin', 'Admin'), ('Nhân viên', 'Employee'), ('Tiểu thương hoặc danh nghiệp', 'Supplier')], default='Cá nhân', max_length=50),
        ),
    ]
