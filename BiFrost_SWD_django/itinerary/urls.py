from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("add/", views.add, name="add"),
    path("edit/<int:trip_id>/", views.edit, name="edit"),
    path("edit/<int:trip_id>/add-event/", views.add_event, name="add_event"),
]
