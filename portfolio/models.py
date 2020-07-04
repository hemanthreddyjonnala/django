from django.db import models


# Create your models here.
class UserPortfolio(models.Model):
    ticker = models.CharField(max_length=20)
    shares = models.FloatField(null=True, blank=True, default=None)
    avg_price = models.FloatField(null=True, blank=True, default=None)
    cost_bought = models.FloatField(null=True, blank=True, default=None)
    current_value = models.FloatField(null=True, blank=True, default=None)
    gain = models.FloatField(null=True, blank=True, default=None)
    account = models.CharField(max_length=20, blank= True)
    user = models.CharField(max_length=100, blank=True)
