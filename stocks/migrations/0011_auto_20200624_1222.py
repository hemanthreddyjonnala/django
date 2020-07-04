# Generated by Django 3.0.7 on 2020-06-24 16:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stocks', '0010_stockticker_vol_trend'),
    ]

    operations = [
        migrations.AddField(
            model_name='stockticker',
            name='price_per_change',
            field=models.FloatField(blank=True, default=None, null=True),
        ),
        migrations.AddField(
            model_name='stockticker',
            name='vol_per_change',
            field=models.FloatField(blank=True, default=None, null=True),
        ),
    ]