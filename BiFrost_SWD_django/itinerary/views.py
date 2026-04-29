from django.shortcuts import render, get_object_or_404, redirect
from .models import Itinerary, Event, TransportationEvent, FoodEvent, EntertainmentEvent


def index(request):
<<<<<<< HEAD
    """
    Acts as the main dashboard.
    Queries the Data Tier for all existing itineraries.
    """
    # Fetching all trips from Postgres
    trips = Itinerary.objects.all()

    return render(request, "itinerary/index.html", {"trips": trips})


def add(request):
    """
    Handles the 'Itinerary Creation' scenario from your Design Doc.
    Moves from the Client Tier (Form) to the Data Tier (Save).
    """
    if request.method == "POST":
        # Extracting data from the POST request
        # Matching the attributes from your UML diagram
        Itinerary.objects.create(
            name=request.POST.get("name"),
            trip_destination=request.POST.get("destination"),
            start_date=request.POST.get("start_date"),
            end_date=request.POST.get("end_date"),
            number_of_participants=request.POST.get("participants", 1),
            user=request.user,
        )
        return redirect("index")

    return render(request, "itinerary/add.html")


def edit(request, trip_id):
    """
    The 'Management' view.
    Demonstrates encapsulation by bundling a trip with all its
    related child events (Transportation, Food, etc.)
    """
    # 1. Get the specific trip or fail gracefully with a 404
    trip = get_object_or_404(Itinerary, id=trip_id)

    # 2. Leveraging the ForeignKey relationship from your UML.
    # This pulls all specialized events (Food, Transport, etc.)
    # attached to this specific Itinerary ID.
    events = trip.events.all()

    context = {
        "trip": trip,
        "events": events,
    }
    return render(request, "itinerary/edit.html", context)


def add_event(request, trip_id):
    trip = get_object_or_404(Itinerary, id=trip_id)

    if request.method == "POST":
        # 1. Grab the "Specialty" type from the form
        event_type = request.POST.get("category")

        # 2. Extract shared data
        event_data = {
            "itinerary": trip,
            "name": request.POST.get("name"),
            "category": event_type,
            "location": request.POST.get("location"),
            "cost": request.POST.get("cost", 0),
            "date": request.POST.get("date"),
            "time": request.POST.get("time"),
        }

        # 3. Decision Logic: Which specialized table do we save to?
        if event_type == "Transportation":
            TransportationEvent.objects.create(
                **event_data, type=1
            )  # Defaulting type to 1 for demo
        elif event_type == "Food":
            FoodEvent.objects.create(**event_data, menu=request.POST.get("detail"))
        else:
            EntertainmentEvent.objects.create(
                **event_data, description=request.POST.get("detail")
            )

        return redirect("edit", trip_id=trip.id)

    return render(request, "itinerary/add_event.html", {"trip": trip})
=======
    return HttpResponse("Itinerary index")

def create_itinerary(request):
    return HttpResponse("Create itinerary")

def edit_itinerary(request, pk):
    return HttpResponse(f"Edit itinerary {pk}")
>>>>>>> a39b742ef2581b72a0cd62fcb37dcb1a444d17af
