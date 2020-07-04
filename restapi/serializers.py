from rest_framework import serializers
from stocks.models import StockTicker

class TickerSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = StockTicker
        fields = ['ticker', 'url','company_name', 'trend', 'vol_trend']