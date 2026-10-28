from django import forms
from django.utils import timezone
from .models import Booking

class BookingForm(forms.ModelForm):
    reservation_date = forms.DateField(
        widget=forms.DateInput(attrs={"type": "date", "id": "reservation_date"}),
        input_formats=["%Y-%m-%d"],
    )
    reservation_slot = forms.TypedChoiceField(
        choices=Booking.TIME_SLOTS,
        coerce=int,
        widget=forms.Select(attrs={"id": "reservation_slot"}),
    )

    class Meta:
        model = Booking
        fields = ["first_name", "reservation_date", "reservation_slot"]
        labels = {
            "first_name": "First name",
            "reservation_date": "Reservation date",
            "reservation_slot": "Reservation slot",
        }
        widgets = {
            "first_name": forms.TextInput(attrs={"placeholder": "Your Name", "autocomplete": "given-name"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.is_bound and not self.initial.get("reservation_date"):
            self.initial["reservation_date"] = timezone.localdate()

    def clean(self):
        cleaned = super().clean()
        date = cleaned.get("reservation_date")
        slot = cleaned.get("reservation_slot")
        if date and slot is not None and Booking.objects.filter(
            reservation_date=date, reservation_slot=slot
        ).exists():
            self.add_error("reservation_slot", "That time is already booked. Please choose another slot.")
        return cleaned
