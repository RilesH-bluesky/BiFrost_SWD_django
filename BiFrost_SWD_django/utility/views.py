from django.shortcuts import render, get_object_or_404
from .models import Place, Alert
from itinerary.models import Itinerary
from django.contrib.auth.decorators import login_required

@login_required
def map_view(request, place_id):
    """
    Map/Utility Workflow: Displays specific geographical data.
    """
    place = get_object_or_404(Place, id=place_id)
    return render(request, "utility/map.html", {"place": place})

@login_required
def alerts_view(request, trip_id):
    """
    System Notification Workflow: Displays alerts for a specific itinerary.
    """
    trip = get_object_or_404(Itinerary, id=trip_id)

    # Fetch alerts linked to this trip
    alerts = Alert.objects.filter(itinerary=trip).order_by("-timestamp")

    return render(request, "utility/alerts.html", {"alerts": alerts, "trip": trip})
