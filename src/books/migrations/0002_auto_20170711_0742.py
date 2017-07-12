# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-07-11 07:42
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='is_banner',
            field=models.CharField(choices=[('On', 'on'), ('Off', 'off')], max_length=10),
        ),
        migrations.AlterField(
            model_name='book',
            name='is_featured',
            field=models.CharField(choices=[('On', 'on'), ('Off', 'off')], max_length=10),
        ),
    ]