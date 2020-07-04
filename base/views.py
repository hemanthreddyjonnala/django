from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.apps import apps



def get_tables():
    env_apps = ['stocks', 'base', 'analytics']
    tables = []
    for app in env_apps:
        for key in apps.all_models[app].keys():
            tables.append(f"{app}_{key}")
    return tables


tables = get_tables()


def home(request):
    data={}
    data['tables']= tables
    data['title'] = 'Joy'
    return render(request, 'base/welcome.html', data)