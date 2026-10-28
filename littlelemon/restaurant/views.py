import json
from datetime import date
from django.db import IntegrityError, transaction
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.utils import timezone
from .forms import BookingForm
from .models import Booking

def home(request):
    return render(request, "restaurant/home.html")

def book(request):
    if request.method == "POST":
        form = BookingForm(request.POST)
        if form.is_valid():
            try:
                with transaction.atomic():
                    form.save()
                return redirect("book")
            except IntegrityError:
                form.add_error("reservation_slot", "That time was just booked. Please choose another slot.")
    else:
        form = BookingForm(initial={"reservation_date": timezone.localdate()})
    return render(request, "restaurant/book.html", {"form": form})

def _booking_data(queryset):
    return [
        {
            "id": booking.pk,
            "first_name": booking.first_name,
            "reservation_date": booking.reservation_date.isoformat(),
            "reservation_slot": booking.reservation_slot,
            "reservation_time": booking.get_reservation_slot_display(),
        }
        for booking in queryset
    ]

def bookings_api(request):
    if request.method != "GET":
        return JsonResponse({"error": "Method not allowed"}, status=405)
    queryset = Booking.objects.all()
    date_value = request.GET.get("date")
    if date_value:
        try:
            date.fromisoformat(date_value)
        except ValueError:
            return JsonResponse({"error": "Use date format YYYY-MM-DD."}, status=400)
        queryset = queryset.filter(reservation_date=date_value)
    return JsonResponse(_booking_data(queryset), safe=False)

def reservations(request):
    return render(request, "restaurant/reservations.html")
