from django.urls import path

from . import views

urlpatterns = [
    path('', views.jupyter_open, name='jupyter-open'),
    ]
