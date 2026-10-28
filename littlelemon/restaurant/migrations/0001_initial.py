from django.db import migrations, models
import django.core.validators

class Migration(migrations.Migration):
    initial = True
    dependencies = []
    operations = [
        migrations.CreateModel(
            name="Booking",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("first_name", models.CharField(max_length=100)),
                ("reservation_date", models.DateField()),
                ("reservation_slot", models.PositiveSmallIntegerField(
                    choices=[(10, "10 AM"), (11, "11 AM"), (12, "12 PM"), (13, "1 PM"), (14, "2 PM"), (15, "3 PM"), (16, "4 PM"), (17, "5 PM"), (18, "6 PM"), (19, "7 PM"), (20, "8 PM")],
                    validators=[django.core.validators.MinValueValidator(10), django.core.validators.MaxValueValidator(20)],
                )),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
            options={
                "ordering": ["reservation_date", "reservation_slot"],
                "constraints": [
                    models.UniqueConstraint(fields=("reservation_date", "reservation_slot"), name="unique_booking_date_and_slot")
                ],
            },
        ),
    ]
