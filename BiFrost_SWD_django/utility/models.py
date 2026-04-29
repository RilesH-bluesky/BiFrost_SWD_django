from django.db import models
from django.contrib.auth.models import User

class Place(models.Model):
    name = models.CharField(max_length=200)
    address = models.CharField(max_length=300, blank=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    price_level = models.IntegerField(null=True, blank=True)
    external_id = models.CharField(max_length=200, blank=True)
    category = models.CharField(max_length=100, blank=True)

class Alert(models.Model):
    itinerary = models.ForeignKey("itinerary.Itinerary", on_delete=models.CASCADE, related_name="alerts")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="alerts")
    timestamp = models.DateTimeField(auto_now_add=True)
    message = models.TextField()
    type = models.CharField(max_length=50)
    is_read = models.BooleanField(default=False)
