from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from rest_framework import serializers
from .models import Booking, Category, MenuItem, Cart, Order, OrderItem

User = get_user_model()

class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ["id", "first_name", "reservation_date", "reservation_slot", "created_at"]
        read_only_fields = ["id", "created_at"]

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "title", "slug"]

class MenuItemSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(), source="category", write_only=True)
    class Meta:
        model = MenuItem
        fields = ["id", "title", "price", "featured", "category", "category_id"]

class CartSerializer(serializers.ModelSerializer):
    menuitem_id = serializers.PrimaryKeyRelatedField(queryset=MenuItem.objects.all(), source="menuitem", write_only=True)
    menuitem = MenuItemSerializer(read_only=True)
    class Meta:
        model = Cart
        fields = ["id", "menuitem", "menuitem_id", "quantity", "unit_price", "price"]
        read_only_fields = ["id", "unit_price", "price"]
    def create(self, validated_data):
        user = self.context["request"].user
        item = validated_data["menuitem"]
        quantity = validated_data["quantity"]
        cart, created = Cart.objects.get_or_create(
            user=user, menuitem=item,
            defaults={"quantity": quantity, "unit_price": item.price, "price": item.price * quantity}
        )
        if not created:
            cart.quantity += quantity
            cart.price = cart.unit_price * cart.quantity
            cart.save(update_fields=["quantity", "price"])
        return cart

class OrderItemSerializer(serializers.ModelSerializer):
    menuitem = MenuItemSerializer(read_only=True)
    class Meta:
        model = OrderItem
        fields = ["menuitem", "quantity", "unit_price", "price"]

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    class Meta:
        model = Order
        fields = ["id", "user", "delivery_crew", "status", "total", "date", "items"]
        read_only_fields = ["id", "user", "total", "date", "items"]

class UserBriefSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email"]

class GroupUserSerializer(serializers.Serializer):
    username = serializers.CharField()
