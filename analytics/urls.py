from django.urls import path
from . import views

urlpatterns = [
    path('', views.price_chart, name='price_chart'),
    path('data', views.pivot_data, name='pivot_data'),
]