from django.shortcuts import render, HttpResponse

# Create your views here.
def index(request):
    return HttpResponse(request, "This is the Itinerary Home Page")

def add(request):
    return HttpResponse(request, "This is where you create an Itinerary")

def edit(request):
    return HttpResponse(request, "This is where you edit an Itinerary")
