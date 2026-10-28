from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

class Booking(models.Model):
    TIME_SLOTS = [(hour, f"{hour % 12 or 12} {'AM' if hour < 12 else 'PM'}") for hour in range(10, 21)]
    first_name = models.CharField(max_length=100)
    reservation_date = models.DateField()
    reservation_slot = models.PositiveSmallIntegerField(
        choices=TIME_SLOTS,
        validators=[MinValueValidator(10), MaxValueValidator(20)],
    )
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ["reservation_date", "reservation_slot"]
        constraints = [models.UniqueConstraint(fields=["reservation_date", "reservation_slot"], name="unique_booking_date_and_slot")]
    def __str__(self):
        return f"{self.first_name} - {self.reservation_date} - {self.get_reservation_slot_display()}"

class Category(models.Model):
    title = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(max_length=255, unique=True)
    def __str__(self):
        return self.title

class MenuItem(models.Model):
    title = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=6, decimal_places=2, validators=[MinValueValidator(0)])
    featured = models.BooleanField(default=False)
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name="menu_items")
    def __str__(self):
        return self.title

class Cart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="cart_items")
    menuitem = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField(validators=[MinValueValidator(1)])
    unit_price = models.DecimalField(max_digits=6, decimal_places=2)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    class Meta:
        constraints = [models.UniqueConstraint(fields=["user", "menuitem"], name="unique_cart_item_per_user")]

class Order(models.Model):
    STATUS_CHOICES = [(0, "Out for delivery"), (1, "Delivered")]
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="orders")
    delivery_crew = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name="assigned_orders")
    status = models.SmallIntegerField(choices=STATUS_CHOICES, default=0)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    date = models.DateTimeField(auto_now_add=True)

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    menuitem = models.ForeignKey(MenuItem, on_delete=models.PROTECT)
    quantity = models.PositiveSmallIntegerField(validators=[MinValueValidator(1)])
    unit_price = models.DecimalField(max_digits=6, decimal_places=2)
    price = models.DecimalField(max_digits=8, decimal_places=2)
