from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import Itinerary, Event, TransportationEvent, FoodEvent, EntertainmentEvent


def index(request):
    """Acts as the main dashboard."""
    trips = Itinerary.objects.all()
    return render(request, "itinerary/index.html", {"trips": trips})


def add(request):
    """Handles the 'Itinerary Creation' scenario."""
    if request.method == "POST":
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
    """The 'Management' view for a specific trip."""
    trip = get_object_or_404(Itinerary, id=trip_id)
    events = trip.events.all()

    return render(request, "itinerary/edit.html", {"trip": trip, "events": events})


def add_event(request, trip_id):
    """Workflow to attach specialized events to an itinerary."""
    trip = get_object_or_404(Itinerary, id=trip_id)

    if request.method == "POST":
        event_type = request.POST.get("category")

        # Safely convert cost to float/decimal for the new merged model
        try:
            cost_val = float(request.POST.get("cost", 0))
        except ValueError:
            cost_val = 0.00

        event_data = {
            "itinerary": trip,
            "name": request.POST.get("name"),
            "category": event_type,
            "location": request.POST.get("location"),
            "cost": cost_val,
            # Fallback to current time if forms don't provide datetime perfectly
            "start_datetime": timezone.now(),
        }

        # Decision Logic routing
        if event_type == "Transportation":
            TransportationEvent.objects.create(**event_data, type=1)
        elif event_type == "Food":
            FoodEvent.objects.create(**event_data, menu=request.POST.get("detail"))
        else:
            EntertainmentEvent.objects.create(
                **event_data, description=request.POST.get("detail")
            )

        return redirect("edit", trip_id=trip.id)

    return render(request, "itinerary/add_event.html", {"trip": trip})


def event_detail(request, event_id):
    """Drill-down workflow for specific event data."""
    event = get_object_or_404(Event, id=event_id)
    return render(request, "itinerary/event_detail.html", {"event": event})
