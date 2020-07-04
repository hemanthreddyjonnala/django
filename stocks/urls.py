from django.urls import path

from . import views
from .views import StocksView, get_most_active, get_query_results

urlpatterns = [
    path('', StocksView.as_view(), name='stocks-screen'),
    path('active', get_most_active, name='stocks-active'),
    path('query', get_query_results, name='stocks-query'),
    ]
