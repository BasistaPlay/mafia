from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.shortcuts import render, redirect

# Create your views here.

def home(request):
    return render(request, 'mainpage/home.html')
