# Generated by Django 5.1.7 on 2025-03-23 05:29

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('San_HNT', '0014_user_role'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='StateOrder',
            field=models.CharField(choices=[('choxacnhan', 'ChoXacNhan'), ('xacnhan', 'XacNhan'), ('chogiaohang', 'ChoGiaoHang'), ('huy', 'Huy'), ('dahuy', 'DaHuy'), ('dagiao', 'DaGiao')], default='choxacnhan', max_length=20),
        ),
        migrations.CreateModel(
            name='Deals',
            fields=[
                ('NgayTao', models.DateTimeField(auto_now_add=True)),
                ('NgayUpdate', models.DateTimeField(auto_now=True)),
                ('Active', models.BooleanField(default=True)),
                ('DealID', models.AutoField(primary_key=True, serialize=False)),
                ('DealName', models.CharField(max_length=200)),
                ('Discount', models.FloatField()),
                ('EndDate', models.DateTimeField()),
                ('Description', models.TextField(blank=True, null=True)),
                ('Supplier', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='San_HNT.supplier')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='DealProducts',
            fields=[
                ('DealProductID', models.AutoField(primary_key=True, serialize=False)),
                ('ProductID', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='San_HNT.product')),
                ('DealID', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='San_HNT.deals')),
            ],
        ),
    ]
