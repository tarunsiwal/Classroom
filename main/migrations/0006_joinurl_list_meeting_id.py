# Generated by Django 2.2.6 on 2022-07-12 11:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_auto_20220712_1618'),
    ]

    operations = [
        migrations.AddField(
            model_name='joinurl_list',
            name='meeting_id',
            field=models.CharField(default='1', max_length=15),
            preserve_default=False,
        ),
    ]
