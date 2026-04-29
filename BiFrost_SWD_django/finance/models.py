from django.db import models
from django.contrib.auth.models import User
from itinerary.models import Itinerary

class Budget(models.Model):
    itinerary = models.OneToOneField(
        Itinerary, on_delete=models.CASCADE, related_name="budget"
    )
    max_budget = models.DecimalField(max_digits=10, decimal_places=2)
    current_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    currency = models.CharField(max_length=10, default="USD")

    def __str__(self):
        return f"Budget for {self.itinerary.name}"
