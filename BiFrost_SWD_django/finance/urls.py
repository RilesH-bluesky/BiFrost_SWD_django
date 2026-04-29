from django.urls import path
from . import views

urlpatterns = [
    # Nested routing: The budget belongs to the trip
    path(
        "itinerary/<int:trip_id>/dashboard/", views.dashboard, name="finance_dashboard"
    ),
]
