from django.urls import path
from . import views

urlpatterns = [
    path("<int:trip_id>/dashboard/", views.dashboard, name="finance_dashboard"),
]
