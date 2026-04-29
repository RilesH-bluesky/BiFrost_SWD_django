from django.shortcuts import render, get_object_or_404
from itinerary.models import Itinerary
from .models import Budget


def dashboard(request, trip_id):
    """
    Financial Workflow: Calculates and displays budget vs actual costs.
    Demonstrates cross-app relationship (Finance talking to Itinerary).
    """
    trip = get_object_or_404(Itinerary, id=trip_id)

    # Demo Safety Net: If a budget doesn't exist for this trip yet, create a dummy one
    budget, created = Budget.objects.get_or_create(
        itinerary=trip,
        defaults={"max_budget": 2500.00, "current_cost": 450.00, "currency": "USD"},
    )

    remaining_budget = budget.max_budget - budget.current_cost

    context = {
        "itinerary": trip,
        "budget": budget,
        "remaining_budget": remaining_budget,
    }
    return render(request, "finance/dashboard.html", context)
