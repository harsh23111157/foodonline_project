from django.shortcuts import render
from . import views

# Create your views here.

def vprofile(request):
    return render(request,'vendor/vprofile.html')