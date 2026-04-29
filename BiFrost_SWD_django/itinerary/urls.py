from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("add/", views.add, name="add"),
    path("edit/<int:trip_id>/", views.edit, name="edit"),
    path("edit/<int:trip_id>/add-event/", views.add_event, name="add_event"),
    path("event/<int:event_id>/", views.event_detail, name="event_detail"),
    path("edit/<int:trip_id>/delete/", views.delete_trip, name="delete_trip"),
    path("event/<int:event_id>/delete/", views.delete_event, name="delete_event"),
]
