# Generated by Django 2.2.6 on 2022-07-13 11:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_auto_20220712_1204'),
    ]

    operations = [
        migrations.AlterField(
            model_name='additional_fiels',
            name='user',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
