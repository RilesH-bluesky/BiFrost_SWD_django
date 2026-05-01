from __future__ import annotations
from abc import ABC, abstractmethod
from django.utils import timezone

from .models import Itinerary, TransportationEvent, FoodEvent, EntertainmentEvent

class EventBuilder(ABC):

    def __init__(self, itinerary: Itinerary) -> None:
        self._itinerary = itinerary
        self._base: dict = {}

    def set_base_fields(
        self,
        *,
        name: str,
        category: str,
        location: str = "",
        cost: float = 0.0,
        start_datetime=None,
        description: str = "",
        order: int = 0,
    ) -> "EventBuilder":

        self._base = {
            "itinerary": self._itinerary,
            "name": name,
            "category": category,
            "location": location,
            "cost": cost,
            "start_datetime": start_datetime or timezone.now(),
            "description": description,
            "order": order,
        }
        return self  

    @abstractmethod
    def build(self, **kwargs):

        ...

class TransportationEventBuilder(EventBuilder):

    def build(self, *, transport_type: int = 1, **kwargs) -> TransportationEvent:
        if not self._base:
            raise RuntimeError(
                "Call set_base_fields() before build()."
            )
        return TransportationEvent.objects.create(
            **self._base,
            type=transport_type,
        )


class FoodEventBuilder(EventBuilder):

    def build(self, *, menu: str = "", **kwargs) -> FoodEvent:
        if not self._base:
            raise RuntimeError(
                "Call set_base_fields() before build()."
            )
        return FoodEvent.objects.create(
            **self._base,
            menu=menu,
        )


class EntertainmentEventBuilder(EventBuilder):

    def build(self, **kwargs) -> EntertainmentEvent:
        if not self._base:
            raise RuntimeError(
                "Call set_base_fields() before build()."
            )
        return EntertainmentEvent.objects.create(**self._base)

class EventDirector:

    def __init__(self, builder: EventBuilder) -> None:
        self._builder = builder

    def construct(
        self,
        *,
        name: str,
        category: str,
        location: str = "",
        cost: float = 0.0,
        start_datetime=None,
        description: str = "",
        order: int = 0,
        **product_kwargs,
    ):

        self._builder.set_base_fields(
            name=name,
            category=category,
            location=location,
            cost=cost,
            start_datetime=start_datetime,
            description=description,
            order=order,
        )
        return self._builder.build(**product_kwargs)
