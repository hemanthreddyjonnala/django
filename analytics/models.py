from django.db import models


# Create your models here.
class PriceInfo(models.Model):
    ticker = models.CharField(max_length=20)
    volume = models.IntegerField(default=0)
    open = models.FloatField(null=True, blank=True, default=None)
    close = models.FloatField(null=True, blank=True, default=None)
    high = models.FloatField(null=True, blank=True, default=None)
    low = models.FloatField(null=True, blank=True, default=None)
    adj_close = models.FloatField(null=True, blank=True, default=None)
    date = models.DateTimeField(default=None, blank=True)
