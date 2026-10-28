from decimal import Decimal
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.db import transaction
from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions, status, viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.exceptions import PermissionDenied, ValidationError
from rest_framework.response import Response
from .models import Booking, Category, MenuItem, Cart, Order, OrderItem
from .serializers import BookingSerializer, CategorySerializer, MenuItemSerializer, CartSerializer, OrderSerializer, UserBriefSerializer, GroupUserSerializer
from .permissions import IsManagerOrReadOnly, IsManager, in_group

User = get_user_model()

class BookingListCreateView(generics.ListCreateAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [permissions.AllowAny]

class BookingDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [permissions.AllowAny]

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all().order_by("title")
    serializer_class = CategorySerializer
    permission_classes = [IsManagerOrReadOnly]

class MenuItemViewSet(viewsets.ModelViewSet):
    queryset = MenuItem.objects.select_related("category").all().order_by("id")
    serializer_class = MenuItemSerializer
    permission_classes = [IsManagerOrReadOnly]
    filterset_fields = ["category", "featured"]
    search_fields = ["title", "category__title"]
    ordering_fields = ["price", "title"]
    ordering = ["title"]

@api_view(["GET", "POST", "DELETE"])
@permission_classes([permissions.IsAuthenticated])
def cart_items(request):
    if request.method == "GET":
        return Response(CartSerializer(Cart.objects.filter(user=request.user).select_related("menuitem", "menuitem__category"), many=True).data)
    if request.method == "DELETE":
        Cart.objects.filter(user=request.user).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    serializer = CartSerializer(data=request.data, context={"request": request})
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data, status=status.HTTP_201_CREATED)

class OrderListCreateView(generics.ListCreateAPIView):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]
    def get_queryset(self):
        user = self.request.user
        if user.is_staff or in_group(user, "Manager"):
            return Order.objects.all().select_related("user", "delivery_crew").prefetch_related("items__menuitem__category")
        if in_group(user, "Delivery Crew"):
            return Order.objects.filter(delivery_crew=user).select_related("user", "delivery_crew").prefetch_related("items__menuitem__category")
        return Order.objects.filter(user=user).select_related("user", "delivery_crew").prefetch_related("items__menuitem__category")
    def create(self, request, *args, **kwargs):
        if request.user.is_staff or in_group(request.user, "Manager") or in_group(request.user, "Delivery Crew"):
            raise PermissionDenied("Only customers can create orders from their cart.")
        cart = list(Cart.objects.filter(user=request.user).select_related("menuitem"))
        if not cart:
            raise ValidationError("Your cart is empty.")
        with transaction.atomic():
            total = sum((item.price for item in cart), Decimal("0.00"))
            order = Order.objects.create(user=request.user, total=total)
            OrderItem.objects.bulk_create([
                OrderItem(order=order, menuitem=item.menuitem, quantity=item.quantity, unit_price=item.unit_price, price=item.price)
                for item in cart
            ])
            Cart.objects.filter(user=request.user).delete()
        order = self.get_queryset().get(pk=order.pk)
        return Response(self.get_serializer(order).data, status=status.HTTP_201_CREATED)

class OrderDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ["get", "patch", "delete", "head", "options"]
    def get_queryset(self):
        user = self.request.user
        if user.is_staff or in_group(user, "Manager"):
            return Order.objects.all().select_related("user", "delivery_crew").prefetch_related("items__menuitem__category")
        if in_group(user, "Delivery Crew"):
            return Order.objects.filter(delivery_crew=user).select_related("user", "delivery_crew").prefetch_related("items__menuitem__category")
        return Order.objects.filter(user=user).select_related("user", "delivery_crew").prefetch_related("items__menuitem__category")
    def partial_update(self, request, *args, **kwargs):
        order = self.get_object()
        if request.user.is_staff or in_group(request.user, "Manager"):
            allowed = {"delivery_crew", "status"}
            if set(request.data.keys()) - allowed:
                raise PermissionDenied("Managers may only change delivery_crew and status.")
            if "delivery_crew" in request.data:
                try:
                    crew_group = Group.objects.get(name="Delivery Crew")
                    crew = User.objects.get(pk=request.data["delivery_crew"], groups=crew_group)
                except (Group.DoesNotExist, User.DoesNotExist, ValueError):
                    raise ValidationError({"delivery_crew": "Select an existing delivery crew user."})
                order.delivery_crew = crew
            if "status" in request.data:
                try:
                    order.status = int(request.data["status"])
                except (ValueError, TypeError):
                    raise ValidationError({"status": "Status must be 0 or 1."})
                if order.status not in (0, 1):
                    raise ValidationError({"status": "Status must be 0 or 1."})
        elif in_group(request.user, "Delivery Crew"):
            if set(request.data.keys()) != {"status"}:
                raise PermissionDenied("Delivery crew may only update order status.")
            try:
                status_value = int(request.data["status"])
            except (ValueError, TypeError):
                raise ValidationError({"status": "Status must be 0 or 1."})
            if status_value not in (0, 1):
                raise ValidationError({"status": "Status must be 0 or 1."})
            order.status = status_value
        else:
            raise PermissionDenied("Customers cannot update orders.")
        order.save()
        return Response(self.get_serializer(order).data)

class GroupUsersView(generics.ListCreateAPIView):
    permission_classes = [IsManager]
    serializer_class = UserBriefSerializer
    def group(self):
        group, _ = Group.objects.get_or_create(name=self.kwargs["group_name"])
        return group
    def get_queryset(self):
        return User.objects.filter(groups=self.group()).order_by("username")
    def create(self, request, *args, **kwargs):
        serializer = GroupUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = get_object_or_404(User, username=serializer.validated_data["username"])
        user.groups.add(self.group())
        return Response(UserBriefSerializer(user).data, status=status.HTTP_201_CREATED)
