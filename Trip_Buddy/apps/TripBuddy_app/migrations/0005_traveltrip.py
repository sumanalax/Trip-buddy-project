# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-08-19 17:06
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TripBuddy_app', '0004_delete_traveltrip'),
    ]

    operations = [
        migrations.CreateModel(
            name='TravelTrip',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('destination', models.CharField(max_length=255)),
                ('description', models.CharField(max_length=255)),
                ('travel_date_from', models.DateField(auto_now_add=True)),
                ('travel_date_to', models.DateField(auto_now=True)),
                ('user_id', models.IntegerField()),
            ],
        ),
    ]
