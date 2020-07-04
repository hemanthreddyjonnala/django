from django.db import models


class StockTicker(models.Model):
    ticker = models.CharField(max_length=20)
    market_cap = models.CharField(max_length=10, blank=True)
    trend = models.IntegerField(default=0)
    sp_500 = models.CharField(max_length=6, blank=True)
    per_day_change = models.FloatField(null=True, blank=True, default=None)
    previous_close = models.FloatField(null=True, blank=True, default=None)
    volume = models.IntegerField(default=0)
    per_50_mva = models.FloatField(null=True, blank=True, default=None)
    per_200_mva = models.FloatField(null=True, blank=True, default=None)
    per_52_low = models.FloatField(null=True, blank=True, default=None)
    per_52_high = models.FloatField(null=True, blank=True, default=None)
    target_est_year = models.FloatField(null=True, blank=True, default=None)
    eps_ttm = models.CharField(max_length=10, blank=True)
    pe_ttm = models.CharField(max_length=10, blank=True)
    forward_pe = models.CharField(max_length=10, blank=True)
    peg_ratio = models.CharField(max_length=10, blank=True)
    book_price = models.CharField(max_length=10, blank=True)
    book_sales = models.CharField(max_length=10, blank=True)
    profit_margin = models.CharField(max_length=10, blank=True)
    current_ratio = models.CharField(max_length=10, blank=True)
    avg_vol_three_month = models.CharField(max_length=20, blank=True)
    company_name = models.CharField(max_length=200, blank=True)
    price_intraday = models.CharField(max_length=20, blank=True)
    vol_trend = models.IntegerField(default=0)
    price_per_change = models.FloatField(null=True, blank=True, default=None)
    vol_per_change = models.FloatField(null=True, blank=True, default=None)

