from django.urls import path
from . import views

urlpatterns = [
<<<<<<< HEAD
    path("", views.index, name="index"),
    path("add/", views.add, name="add"),
    path("edit/<int:trip_id>/", views.edit, name="edit"),
    path("edit/<int:trip_id>/add-event/", views.add_event, name="add_event"),
=======
    path("", views.index, name="itinerary_index"),
    path("create/", views.create_itinerary, name="itinerary_create"),
    path("edit/<int:pk>/", views.edit_itinerary, name="itinerary_edit"),
>>>>>>> a39b742ef2581b72a0cd62fcb37dcb1a444d17af
]
