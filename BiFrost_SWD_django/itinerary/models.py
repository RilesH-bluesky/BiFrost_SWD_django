from django.db import models
from django.contrib.auth.models import User


# ==========================================
# Class 1: Itinerary
# ==========================================
class Itinerary(models.Model):
    """
    Concrete implementation of the Itinerary Interface.
    Acts as the master container for trip information.
    """

    # Core UML attributes maintained for view compatibility
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="itineraries")
    name = models.CharField(max_length=200, help_text="Maps UML 'name: str'")
    trip_destination = models.CharField(
        max_length=255, help_text="Maps UML 'trip_destination: str'"
    )

    # Upgraded to DateField based on practical system requirements
    start_date = models.DateField(help_text="Maps UML 'start_date: DateTime'")
    end_date = models.DateField(help_text="Maps UML 'end_date: DateTime'")

    number_of_participants = models.PositiveIntegerField(
        default=1, help_text="Maps UML 'number_of_participants: int'"
    )
    itinerary_events = models.IntegerField(
        default=0, help_text="Static field mapping UML requirement."
    )

    # Modern features added via merge
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} Trip to {self.trip_destination}"


# ==========================================
# Class 2: Event (Parent - Multi-Table Inheritance)
# ==========================================
class Event(models.Model):
    """
    Parent class derived from <<abstract>> Events UML box.
    Stores attributes shared by all specialized event types.
    """

    # Core structural relationships
    itinerary = models.ForeignKey(
        Itinerary, on_delete=models.CASCADE, related_name="events"
    )
    place = models.ForeignKey(
        "utility.Place",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="events",
    )

    # UML Base Attributes
    name = models.CharField(max_length=200, help_text="Maps UML 'name: str'")
    category = models.CharField(max_length=50, help_text="Maps UML 'category: str'")
    location = models.CharField(
        max_length=255, blank=True, help_text="Maps UML 'location: str'"
    )

    # Upgraded cost to handle real-world currency values
    cost = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Maps UML 'cost: int'",
    )

    # Unification of Date and Time tracking strategies
    date = models.DateField(
        null=True, blank=True, help_text="Maps UML 'date: DateTime'"
    )
    time = models.TimeField(
        null=True, blank=True, help_text="Maps UML 'time: DateTime'"
    )
    start_datetime = models.DateTimeField(null=True, blank=True)
    end_datetime = models.DateTimeField(null=True, blank=True)

    # UI and sorting metadata
    description = models.TextField(
        blank=True, help_text="Consolidated description field"
    )
    order = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.name} ({self.category}) for trip: {self.itinerary.name}"


# ==========================================
# Specialized Child Classes (Inheritance)
# ==========================================


class TransportationEvent(Event):
    """
    Specialized event derived from Transportation Event UML box.
    """

    TYPE_CHOICES = [
        (1, "Flight"),
        (2, "Train"),
        (3, "Bus"),
        (4, "Rental Car"),
        (5, "Walk/Other"),
    ]
    type = models.IntegerField(choices=TYPE_CHOICES, help_text="Maps UML 'type: int'")


class FoodEvent(Event):
    """
    Specialized event derived from Food Event UML box.
    """

    menu = models.TextField(blank=True, null=True, help_text="Maps UML 'menu: str'")


class EntertainmentEvent(Event):
    """
    Specialized event derived from Entertainment Event UML box.
    """

    # The 'description' attribute required by UML is now inherited directly
    # from the parent Event class to prevent database collisions.
    pass
