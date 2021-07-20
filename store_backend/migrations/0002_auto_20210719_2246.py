# Generated by Django 3.2 on 2021-07-19 18:16

import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('store_backend', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='storeuser',
            name='user_ptr',
        ),
        migrations.AlterField(
            model_name='category',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='product',
            name='category',
            field=models.ForeignKey(default='دسته بندی نشده', on_delete=django.db.models.deletion.SET_DEFAULT, to='store_backend.category'),
        ),
        migrations.AlterField(
            model_name='product',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.CreateModel(
            name='Receipt',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('numOfPurchase', models.IntegerField()),
                ('name', models.CharField(max_length=512)),
                ('familyName', models.CharField(max_length=512)),
                ('address', models.CharField(max_length=1024)),
                ('totalPrice', models.FloatField()),
                ('dateOfPurchase', models.DateTimeField()),
                ('trackingCode', models.IntegerField()),
                ('productName', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store_backend.product')),
            ],
        ),
    ]