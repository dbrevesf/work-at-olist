# Generated by Django 2.1.1 on 2018-09-13 14:18

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Call',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('source', models.CharField(max_length=9)),
                ('destination', models.CharField(max_length=9)),
            ],
        ),
    ]
