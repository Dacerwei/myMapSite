# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-04-29 09:09
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ubike', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='lasted_station',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sno', models.IntegerField()),
                ('sna', models.CharField(max_length=100)),
                ('snaen', models.CharField(max_length=100)),
                ('tot', models.IntegerField()),
                ('sbi', models.IntegerField()),
                ('sarea', models.CharField(max_length=100)),
                ('mday', models.CharField(max_length=200)),
                ('lat', models.FloatField()),
                ('lng', models.FloatField()),
                ('ar', models.CharField(max_length=100)),
                ('sareaen', models.CharField(max_length=100)),
                ('aren', models.CharField(max_length=100)),
                ('bemp', models.IntegerField()),
                ('act', models.BooleanField(default=True)),
                ('datetime', models.DateTimeField()),
            ],
        ),
    ]
