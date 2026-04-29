from django.db import models
from django.contrib.auth.models import User

<<<<<<< HEAD

# Create your models here.
# ==========================================
# Class 1: Itinerary
# ==========================================
class Itinerary(models.Model):
    """
    Concrete implementation of the Itinerary Interface.
    Acts as the master container for trip information.
    """

    # Implicit link required by design document (not in specific image box)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="itineraries")

    # Attributes mapped verbatim from image_2.png Itinerary box:
    name = models.CharField(max_length=200, help_text="Maps UML 'name: str'")
    trip_destination = models.CharField(
        max_length=255, help_text="Maps UML 'trip_destination: str'"
    )
    start_date = models.DateTimeField(help_text="Maps UML 'start_date: DateTime'")
    end_date = models.DateTimeField(help_text="Maps UML 'end_date: DateTime'")
    number_of_participants = models.PositiveIntegerField(
        default=1, help_text="Maps UML 'number_of_participants: int'"
    )

    # Redundant derived attribute mapped verbatim. In best practices,
    # this would be calculated by a method, not stored as a static field.
    # We include it here strictly to fulfill the literal UML translation.
    itinerary_events = models.IntegerField(
        default=0,
        help_text="Maps UML 'itinerary_events: int'. Warn: Static field, should be derived.",
    )

    def __str__(self):
        # Basic representation for Django Admin
        return f"{self.name} Trip to {self.trip_destination}"

    # Note: I am omitting explicit getter/setter methods (like getTotalCost(), setTripName())
    # listed in the UML arguments box. Django's Active Record pattern (Model class)
    # provides these automatically. For example, my_itinerary.name = "New Name" handles setting,
    # and my_itinerary.event_set.all() handles getEvents(). Adding explicit getters/setters
    # is unidiomatic and redundant in Python/Django.


# ==========================================
# Class 2: Event (Parent - Multi-Table Inheritance)
# ==========================================
class Event(models.Model):
    """
    Parent class derived from <<abstract>> Events UML box.
    Stores attributes shared by all specialized event types.
    Inheritance structure allows querying Itinerary.events.all() generically.
    """

    # Explicit Directed Relationship mapped from image_2.png dashed arrow:
    # An Event must belong to an Itinerary.
    itinerary = models.ForeignKey(
        Itinerary, on_delete=models.CASCADE, related_name="events"
    )

    # Attributes mapped verbatim from image_2.png <<abstract>> Events box:
    name = models.CharField(max_length=200, help_text="Maps UML 'name: str'")
    category = models.CharField(max_length=100, help_text="Maps UML 'category: str'")
    location = models.CharField(max_length=255, help_text="Maps UML 'location: str'")

    # Currency generally uses DecimalField for accuracy, but mapped as IntegerField literally.
    cost = models.IntegerField(default=0, help_text="Maps UML 'cost: int'")

    # Duplicate DateTime attributes listed in UML. Redundant design,
    # should be combined or differentiated with DateField/TimeField.
    # Implemented literally as per UML specification.
    date = models.DateTimeField(help_text="Maps UML 'date: DateTime'")
    time = models.DateTimeField(
        help_text="Maps UML 'time: DateTime'. Warn: Duplicate timestamp info."
    )

    def __str__(self):
        # Basic representation showing relationship in Admin
        return f"{self.name} ({self.category}) for trip: {self.itinerary.name}"


# ==========================================
# Specialized Child Classes (Inheritance)
# ==========================================


class TransportationEvent(Event):
    """
    Specialized event derived from Transportation Event UML box.
    Implicitly links to parent Event table.
    """

    # UML adds specialized attribute: type: int
    # Creating choices to map the generic int to meaningful transport types
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
    Implicitly links to parent Event table.
    """

    # UML adds specialized attribute: menu: str
    menu = models.TextField(
        blank=True,
        null=True,
        help_text="Maps UML 'menu: str'. Using TextField for flexible input.",
    )


class EntertainmentEvent(Event):
    """
    Specialized event derived from Entertainment Event UML box.
    Implicitly links to parent Event table.
    """

    # UML adds specialized attribute: description: str
    description = models.TextField(help_text="Maps UML 'description: str'")
=======

class Itinerary(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="itineraries")
    name = models.CharField(max_length=200)
    destination = models.CharField(max_length=200)
    start_date = models.DateField()
    end_date = models.DateField()
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.destination})"


class Budget(models.Model):
    itinerary = models.OneToOneField(
        Itinerary, on_delete=models.CASCADE, related_name="budget"
    )
    max_budget = models.DecimalField(max_digits=10, decimal_places=2)
    current_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    currency = models.CharField(max_length=10, default="USD")

    def __str__(self):
        return f"Budget for {self.itinerary.name}"


class Place(models.Model):
    name = models.CharField(max_length=200)
    address = models.CharField(max_length=300, blank=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    price_level = models.IntegerField(null=True, blank=True)
    external_id = models.CharField(max_length=200, blank=True)  # e.g. Google Place ID
    category = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.name


class Event(models.Model):
    CATEGORY_CHOICES = [
        ("flight", "Flight"),
        ("hotel", "Hotel"),
        ("food", "Food"),
        ("activity", "Activity"),
        ("transport", "Transport"),
        ("other", "Other"),
    ]

    itinerary = models.ForeignKey(
        Itinerary, on_delete=models.CASCADE, related_name="events"
    )
    place = models.ForeignKey(
        Place, on_delete=models.SET_NULL, null=True, blank=True, related_name="events"
    )
    name = models.CharField(max_length=200)
    category = models.CharField(
        max_length=50, choices=CATEGORY_CHOICES, default="other"
    )
    start_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField(null=True, blank=True)
    description = models.TextField(blank=True)
    cost = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["start_datetime", "order"]

    def __str__(self):
        return f"{self.name} ({self.itinerary.name})"


class Alert(models.Model):
    ALERT_TYPE_CHOICES = [
        ("reminder", "Reminder"),
        ("warning", "Warning"),
        ("info", "Info"),
    ]

    itinerary = models.ForeignKey(
        Itinerary, on_delete=models.CASCADE, related_name="alerts"
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="alerts")
    timestamp = models.DateTimeField(auto_now_add=True)
    message = models.TextField()
    type = models.CharField(max_length=50, choices=ALERT_TYPE_CHOICES, default="info")
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ["-timestamp"]

    def __str__(self):
        return f"{self.type} for {self.itinerary.name}"

>>>>>>> a39b742ef2581b72a0cd62fcb37dcb1a444d17af
