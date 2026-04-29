from django.shortcuts import render, HttpResponse

def index(request):
    return HttpResponse("Itinerary index")

def create_itinerary(request):
    return HttpResponse("Create itinerary")

def edit_itinerary(request, pk):
    return HttpResponse(f"Edit itinerary {pk}")
