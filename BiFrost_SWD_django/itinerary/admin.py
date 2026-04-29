from django.contrib import admin
from .models import Itinerary, Budget, Place, Event, Alert

admin.site.register(Itinerary)
admin.site.register(Budget)
admin.site.register(Place)
admin.site.register(Event)
admin.site.register(Alert)
