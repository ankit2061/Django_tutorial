#from django.http import HttpResponse
from django.shortcuts import render

def Homepage(request):
    #return HttpResponse("Hello World! This is my homepage")
    return render(request,'home.html')

def about(request):
    #return HttpResponse("My About Page.")
    return render(request,'about.html')
