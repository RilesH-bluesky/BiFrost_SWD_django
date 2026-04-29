from django.db import transaction
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth import get_user_model

from itinerary.models import (
    Itinerary,
    TransportationEvent,
    FoodEvent,
    EntertainmentEvent,
)
from finance.models import Budget
from utility.models import Place, Alert

User = get_user_model()


def run_seed():
    # The 'atomic' block is your safety net. If ANY line of code fails in here,
    # PostgreSQL will cancel the entire operation. No corrupted half-data.
    with transaction.atomic():
        print("🧹 Cleaning up old demo data...")
        Itinerary.objects.all().delete()
        Place.objects.all().delete()

        print("👤 Setting up Superuser...")
        user, created = User.objects.get_or_create(
            username="root", defaults={"email": "root@root.com"}
        )
        user.set_password("root1234")
        user.save()

        now = timezone.now()

        # ==========================================
        # TRIP 1: Summer in Paris (The Baseline)
        # ==========================================
        print("🌍 Building Trip 1: Paris...")
        place_paris = Place.objects.create(
            name="Le Jules Verne",
            address="Eiffel Tower, 2nd Floor, Paris",
            latitude=48.8584,
            longitude=2.2945,
            price=250.00,
            price_level=4,
            category="Fine Dining",
        )
        place_louvre = Place.objects.create(
            name="The Louvre Museum",
            address="Rue de Rivoli, 75001 Paris",
            price=17.00,
            price_level=2,
            category="Museum",
        )

        trip1 = Itinerary.objects.create(
            user=user,
            name="Summer in Paris",
            trip_destination="Paris, France",
            start_date=now.date() + timedelta(days=30),
            end_date=now.date() + timedelta(days=37),
            number_of_participants=2,
            description="A comprehensive week-long tech and culture tour in Paris.",
        )
        Budget.objects.create(
            itinerary=trip1, max_budget=5000.00, current_cost=1117.00, currency="USD"
        )

        TransportationEvent.objects.create(
            itinerary=trip1,
            name="Delta Flight DL 404 Outbound",
            category="Flight",
            cost=850.00,
            start_datetime=now + timedelta(days=30, hours=8),
            type=1,
        )
        FoodEvent.objects.create(
            itinerary=trip1,
            place=place_paris,
            name="Dinner at Le Jules Verne",
            category="Dining",
            cost=250.00,
            start_datetime=now + timedelta(days=31, hours=19),
            menu="5-Course Tasting Menu",
        )
        EntertainmentEvent.objects.create(
            itinerary=trip1,
            place=place_louvre,
            name="Louvre VIP Tour",
            category="Culture",
            cost=17.00,
            start_datetime=now + timedelta(days=32, hours=10),
            description="Private guided tour.",
        )
        Alert.objects.create(
            itinerary=trip1,
            user=user,
            message="Eurostar Train strike announced. Expect delays.",
            type="warning",
        )

        # ==========================================
        # TRIP 2: London Premier League Weekend
        # ==========================================
        print("⚽ Building Trip 2: London...")
        place_emirates = Place.objects.create(
            name="Emirates Stadium",
            address="Hornsey Rd, London N7 7AJ, UK",
            price=95.00,
            price_level=3,
            category="Sports Venue",
        )

        trip2 = Itinerary.objects.create(
            user=user,
            name="EPL Match Weekend",
            trip_destination="London, UK",
            start_date=now.date() + timedelta(days=14),
            end_date=now.date() + timedelta(days=16),
            number_of_participants=3,
            description="Quick weekend trip to catch the Arsenal game.",
        )
        Budget.objects.create(
            itinerary=trip2, max_budget=1500.00, current_cost=450.00, currency="GBP"
        )

        TransportationEvent.objects.create(
            itinerary=trip2,
            name="Heathrow Express",
            category="Train",
            cost=25.00,
            start_datetime=now + timedelta(days=14, hours=14),
            type=2,  # Train
        )
        EntertainmentEvent.objects.create(
            itinerary=trip2,
            place=place_emirates,
            name="Chelsea Match",
            category="Sports",
            cost=95.00,
            start_datetime=now + timedelta(days=15, hours=15),
            description="Club level seating, section 114.",
        )
        Alert.objects.create(
            itinerary=trip2,
            user=user,
            message="Digital match tickets have been issued.",
            type="info",
            is_read=True,
        )

        # ==========================================
        # TRIP 3: NYC Tech Conference
        # ==========================================
        print("💻 Building Trip 3: New York...")
        place_javits = Place.objects.create(
            name="Javits Center",
            address="429 11th Ave, New York, NY 10001",
            price=0.00,
            price_level=1,
            category="Convention Center",
        )

        trip3 = Itinerary.objects.create(
            user=user,
            name="Backend Engineering Expo",
            trip_destination="New York City, NY",
            start_date=now.date() + timedelta(days=60),
            end_date=now.date() + timedelta(days=63),
            number_of_participants=1,
            description="Attending the annual software architecture summit.",
        )
        Budget.objects.create(
            itinerary=trip3, max_budget=2500.00, current_cost=1200.00, currency="USD"
        )

        TransportationEvent.objects.create(
            itinerary=trip3,
            name="JFK Airport Shuttle",
            category="Bus",
            cost=45.00,
            start_datetime=now + timedelta(days=60, hours=10),
            type=3,  # Bus
        )
        EntertainmentEvent.objects.create(
            itinerary=trip3,
            place=place_javits,
            name="Keynote: Microservices",
            category="Conference",
            cost=0.00,
            start_datetime=now + timedelta(days=61, hours=9),
            description="Main stage presentation on distributed systems.",
        )

        # ==========================================
        # TRIP 4: Local Hiking Retreat
        # ==========================================
        print("⛰️ Building Trip 4: Roan Mountain...")
        place_roan = Place.objects.create(
            name="Roan Mountain State Park",
            address="527 Hwy 143, Roan Mountain, TN",
            price=15.00,
            price_level=1,
            category="National Park",
        )

        trip4 = Itinerary.objects.create(
            user=user,
            name="Strength & Conditioning Retreat",
            trip_destination="Roan Mountain, TN",
            start_date=now.date() + timedelta(days=5),
            end_date=now.date() + timedelta(days=7),
            number_of_participants=2,
            description="4-day gym split translated to outdoor trail hiking.",
        )
        Budget.objects.create(
            itinerary=trip4, max_budget=300.00, current_cost=85.00, currency="USD"
        )

        TransportationEvent.objects.create(
            itinerary=trip4,
            name="Drive to Trailhead",
            category="Car",
            cost=40.00,
            start_datetime=now + timedelta(days=5, hours=7),
            type=4,  # Car
        )
        EntertainmentEvent.objects.create(
            itinerary=trip4,
            place=place_roan,
            name="Carvers Gap Hike",
            category="Fitness",
            cost=0.00,
            start_datetime=now + timedelta(days=5, hours=9),
            description="10-mile round trip on the Appalachian Trail.",
        )
        Alert.objects.create(
            itinerary=trip4,
            user=user,
            message="Weather warning: High winds expected at the summit.",
            type="warning",
        )

        print(
            "\n✅ SUCCESS: 4 complete demo trips successfully injected into PostgreSQL!"
        )


# Execute the function
run_seed()


# Command to run this: cat seed.py | docker compose exec -T web uv run manage.py shell
