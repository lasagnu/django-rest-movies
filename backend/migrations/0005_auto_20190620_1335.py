# Generated by Django 2.2.2 on 2019-06-20 13:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0004_auto_20190620_1330'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movies',
            name='year',
            field=models.TextField(blank=True, default='', max_length=16),
        ),
    ]
