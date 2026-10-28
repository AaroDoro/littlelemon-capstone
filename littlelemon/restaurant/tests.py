from datetime import date, timedelta
from django.contrib.auth.models import User, Group
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Booking, Category, MenuItem

class BookingAPITests(APITestCase):
    def test_create_booking(self):
        response = self.client.post("/api/bookings/", {
            "first_name": "Asha", "reservation_date": str(date.today() + timedelta(days=1)),
            "reservation_slot": 12
        }, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Booking.objects.count(), 1)

    def test_duplicate_booking_rejected(self):
        d = date.today() + timedelta(days=2)
        Booking.objects.create(first_name="Asha", reservation_date=d, reservation_slot=12)
        response = self.client.post("/api/bookings/", {
            "first_name": "Riya", "reservation_date": str(d), "reservation_slot": 12
        }, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

class MenuAPITests(APITestCase):
    def setUp(self):
        self.manager = User.objects.create_user(username="manager", password="Pass12345!")
        group, _ = Group.objects.get_or_create(name="Manager")
        self.manager.groups.add(group)
        self.category = Category.objects.create(title="Mains", slug="mains")
    def test_menu_list_public(self):
        response = self.client.get("/api/menu-items/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    def test_manager_can_create_menu_item(self):
        self.client.force_authenticate(user=self.manager)
        response = self.client.post("/api/menu-items/", {
            "title": "Pasta", "price": "12.50", "featured": False, "category_id": self.category.id
        }, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    def test_customer_cannot_create_menu_item(self):
        customer = User.objects.create_user(username="customer", password="Pass12345!")
        self.client.force_authenticate(user=customer)
        response = self.client.post("/api/menu-items/", {
            "title": "Pasta", "price": "12.50", "featured": False, "category_id": self.category.id
        }, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
