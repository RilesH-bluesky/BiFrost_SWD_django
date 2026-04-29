from django.urls import path
from . import views

urlpatterns = [
    # Flat routing for locations
    path("place/<int:place_id>/", views.map_view, name="map_view"),
    # Nested routing: Alerts belong to a specific trip
    path("<int:trip_id>/alerts/", views.alerts_view, name="alerts_view"),
]
