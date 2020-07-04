from django.shortcuts import render

# Create your views here.
import os
import subprocess
from base.views import tables


def jupyter_open(request):
    cmd = "jupyter notebook"
    # m = os.system(cmd)
    returned_output = subprocess.check_output(cmd)
    data={}
    data['tables']= tables
    data['title'] = 'Joy'
    return render(request, 'base/welcome.html', data)