from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("", views.index, name="add"),
    path("", views.index, name="edit"),
]