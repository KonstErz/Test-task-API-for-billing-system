# Generated by Django 3.0.5 on 2020-04-18 06:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_auto_20200418_1240'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='currency',
            name='wallet',
        ),
    ]
