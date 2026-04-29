from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="itinerary_index"),
    path("create/", views.create_itinerary, name="itinerary_create"),
    path("edit/<int:pk>/", views.edit_itinerary, name="itinerary_edit"),
]
