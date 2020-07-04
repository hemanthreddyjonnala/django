from django.urls import include, path
from . import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register('ticker', views.TickerView)

urlpatterns = [
    path('', include(router.urls)),
    ]