"""
views.py — Itinerary views updated to use the Builder Design Pattern.

Key change: add_event() now delegates object construction to EventDirector
instead of calling ORM .create() directly, making it easy to swap,
extend, or unit-test event creation without touching view logic.
"""

from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.template.loader import render_to_string
from xhtml2pdf import pisa

from .models import Itinerary, Event
from .builders import (
    EventDirector,
    TransportationEventBuilder,
    FoodEventBuilder,
    EntertainmentEventBuilder,
)


@login_required
def index(request):
    trips = Itinerary.objects.filter(user=request.user).order_by("-created_at")
    return render(request, "itinerary/index.html", {"trips": trips})


@login_required
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


@login_required
def edit(request, trip_id):
    trip = get_object_or_404(Itinerary, id=trip_id, user=request.user)
    events = trip.events.all()
    return render(request, "itinerary/edit.html", {"trip": trip, "events": events})


@login_required
def add_event(request, trip_id):

    trip = get_object_or_404(Itinerary, id=trip_id)

    if request.method == "POST":
        event_type = request.POST.get("category")

        try:
            cost_val = float(request.POST.get("cost", 0))
        except ValueError:
            cost_val = 0.00

        
        builder_map = {
            "Transportation": TransportationEventBuilder,
            "Food": FoodEventBuilder,
        }
        BuilderClass = builder_map.get(event_type, EntertainmentEventBuilder)
        director = EventDirector(BuilderClass(itinerary=trip))

        product_kwargs: dict = {}
        if event_type == "Transportation":
            product_kwargs["transport_type"] = 1  # default: Flight
        elif event_type == "Food":
            product_kwargs["menu"] = request.POST.get("detail", "")

        director.construct(
            name=request.POST.get("name", ""),
            category=event_type,
            location=request.POST.get("location", ""),
            cost=cost_val,
            start_datetime=timezone.now(),
            description=request.POST.get("detail", ""),
            **product_kwargs,
        )

        return redirect("edit", trip_id=trip.id)

    return render(request, "itinerary/add_event.html", {"trip": trip})


@login_required
def event_detail(request, event_id):
    """Hybrid view: displays event details and handles Edit saving."""
    event = get_object_or_404(Event, id=event_id, itinerary__user=request.user)

    if request.method == "POST":
        event.name = request.POST.get("name")
        event.location = request.POST.get("location")
        try:
            event.cost = float(request.POST.get("cost", 0))
        except ValueError:
            pass
        event.save()
        return redirect("edit", trip_id=event.itinerary.id)

    return render(request, "itinerary/event_detail.html", {"event": event})


@login_required
def delete_trip(request, trip_id):
    """Deletes an entire itinerary and cascades to all events/budgets."""
    trip = get_object_or_404(Itinerary, id=trip_id, user=request.user)
    if request.method == "POST":
        trip.delete()
        return redirect("index")
    return redirect("edit", trip_id=trip.id)


@login_required
def delete_event(request, event_id):
    """Deletes a single event."""
    event = get_object_or_404(Event, id=event_id, itinerary__user=request.user)
    trip_id = event.itinerary.id
    if request.method == "POST":
        event.delete()
    return redirect("edit", trip_id=trip_id)


@login_required
def export_pdf(request, trip_id):
    trip = get_object_or_404(Itinerary, id=trip_id, user=request.user)
    html = render_to_string("itinerary/pdf_template.html", {"trip": trip})
    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = f'attachment; filename="{trip.name}.pdf"'
    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
        return HttpResponse("PDF generation failed", status=500)
    return response