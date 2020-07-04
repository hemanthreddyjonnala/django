from django.shortcuts import render
from rest_framework import viewsets, permissions
from stocks.models import StockTicker
from .serializers import TickerSerializer

class TickerView(viewsets.ModelViewSet):
    queryset = StockTicker.objects.all()
    serializer_class = TickerSerializer
    permission_classes = (permissions.IsAuthenticated,)