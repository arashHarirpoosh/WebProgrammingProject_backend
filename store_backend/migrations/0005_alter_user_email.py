# Generated by Django 3.2 on 2021-07-19 19:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store_backend', '0004_auto_20210719_2337'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(blank=True, editable=False, max_length=254, unique=True, verbose_name='email address'),
        ),
    ]
