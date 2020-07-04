from django.contrib import admin

# Register your models here.
from .models import StockTicker

admin.site.register(StockTicker)
