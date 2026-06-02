from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

from salon.models import Appointment, Service


SERVICES = [
    {
        "id": 1,
        "name": "Standard Haircut",
        "description": "Clean standard haircut with shaping and finishing.",
        "price": "50000.00",
        "duration_minutes": 45,
    },
    {
        "id": 2,
        "name": "Deep Cleansing Botanical Facial",
        "description": "Organic herbal steam, gentle exfoliation, and a custom hydrating masque.",
        "price": "85000.00",
        "duration_minutes": 60,
    },
    {
        "id": 3,
        "name": "Women's Hair Plaiting",
        "description": "Women's hair plaiting starts at UGX 80,000 and increases depending on the hairstyle.",
        "price": "80000.00",
        "duration_minutes": 120,
    },
    {
        "id": 4,
        "name": "Luxury Gel Manicure & Pedicure",
        "description": "Nail shaping, cuticle care, scrubs, and premium gel-cured polish.",
        "price": "75000.00",
        "duration_minutes": 75,
    },
    {
        "id": 5,
        "name": "Therapeutic Swedish Massage",
        "description": "Relaxing full-body oil massage with soothing pressure for muscular relief.",
        "price": "110000.00",
        "duration_minutes": 90,
    },
]

APPOINTMENTS = [
    {
        "username": "godwin",
        "client_name": "Ssemwogerere Godwin",
        "client_email": "godwin@example.com",
        "service_id": 1,
        "quoted_price": "50000.00",
        "date": "2026-06-05",
        "time_slot": "10:00 AM",
        "status": "Confirmed",
    },
    {
        "username": "christian",
        "client_name": "Christian",
        "client_email": "christian@example.com",
        "service_id": 4,
        "quoted_price": "75000.00",
        "date": "2026-06-05",
        "time_slot": "02:00 PM",
        "status": "Pending",
    },
    {
        "username": "matia",
        "client_name": "Matia",
        "client_email": "matia@example.com",
        "service_id": 2,
        "quoted_price": "85000.00",
        "date": "2026-06-06",
        "time_slot": "11:00 AM",
        "status": "Completed",
    },
]

USERS = [
    {
        "username": "godwin",
        "password": "customer123",
        "first_name": "Ssemwogerere",
        "last_name": "Godwin",
        "email": "godwin@example.com",
        "is_staff": False,
    },
    {
        "username": "christian",
        "password": "customer123",
        "first_name": "Christian",
        "last_name": "",
        "email": "christian@example.com",
        "is_staff": False,
    },
    {
        "username": "matia",
        "password": "customer123",
        "first_name": "Matia",
        "last_name": "",
        "email": "matia@example.com",
        "is_staff": False,
    },
    {
        "username": "angel",
        "password": "customer123",
        "first_name": "Angel",
        "last_name": "",
        "email": "angel@example.com",
        "is_staff": False,
    },
    {
        "username": "barber",
        "password": "barber123",
        "first_name": "Salon",
        "last_name": "Barber",
        "email": "barber@example.com",
        "is_staff": True,
    },
]


class Command(BaseCommand):
    help = "Seed the salon database with demo services and appointments."

    def handle(self, *args, **options):
        users_by_username = {}
        for user_data in USERS:
            password = user_data.pop("password")
            user, _created = User.objects.update_or_create(
                username=user_data["username"],
                defaults=user_data,
            )
            user.set_password(password)
            user.save()
            users_by_username[user.username] = user
            user_data["password"] = password

        for service in SERVICES:
            Service.objects.update_or_create(id=service["id"], defaults=service)

        Appointment.objects.exclude(client_name="Angel").delete()
        for appointment in APPOINTMENTS:
            username = appointment.pop("username")
            client = users_by_username[username]
            Appointment.objects.update_or_create(
                date=appointment["date"],
                time_slot=appointment["time_slot"],
                defaults={**appointment, "client": client},
            )
            appointment["username"] = username

        angel = users_by_username["angel"]
        Appointment.objects.update_or_create(
            date="2026-06-06",
            time_slot="03:00 PM",
            defaults={
                "client_name": "Angel",
                "client_email": "angel@example.com",
                "client": angel,
                "service_id": 3,
                "quoted_price": "110000.00",
                "status": "Pending",
            },
        )

        self.stdout.write(self.style.SUCCESS("Salon demo data is ready."))
