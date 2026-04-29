from django.db import models
from django.contrib.auth.models import User


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

