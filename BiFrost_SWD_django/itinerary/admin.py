from django.contrib import admin
from .models import Itinerary, Event, TransportationEvent, FoodEvent, EntertainmentEvent

admin.site.register(Itinerary)
admin.site.register(Event)
admin.site.register(TransportationEvent)
admin.site.register(FoodEvent)
admin.site.register(EntertainmentEvent)