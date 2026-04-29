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

class Event(models.Model):
    itinerary = models.ForeignKey("itinerary.Itinerary", on_delete=models.CASCADE, related_name="events")
    place = models.ForeignKey("utility.Place", null=True, blank=True, on_delete=models.SET_NULL, related_name="events")
    name = models.CharField(max_length=200)
    category = models.CharField(max_length=50)
    start_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField(null=True, blank=True)
    description = models.TextField(blank=True)
    cost = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    order = models.PositiveIntegerField(default=0)





