# Generated by Django 3.0.7 on 2020-06-24 16:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stocks', '0011_auto_20200624_1222'),
    ]

    operations = [
        migrations.DeleteModel(
            name='SearchTicker',
        ),
    ]