# Generated by Django 2.1.1 on 2018-09-13 19:02

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_auto_20180913_1452'),
    ]

    operations = [
        migrations.CreateModel(
            name='PriceRule',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fixed_price', models.FloatField(default=0.0)),
                ('variable_price', models.FloatField(default=0.0)),
                ('fixed_start_period', models.TimeField()),
                ('fixed_end_period', models.TimeField()),
                ('created_date', models.DateTimeField(default=datetime.datetime.now)),
            ],
        ),
    ]