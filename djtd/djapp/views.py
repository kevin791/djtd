from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
#第一个视图
def index(request):
    return HttpResponse("Hehllo,world.")