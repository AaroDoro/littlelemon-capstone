from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .api_views import BookingListCreateView, BookingDetailView, CategoryViewSet, MenuItemViewSet, cart_items, OrderListCreateView, OrderDetailView, GroupUsersView

router = DefaultRouter()
router.register("categories", CategoryViewSet, basename="category")
router.register("menu-items", MenuItemViewSet, basename="menuitem")

urlpatterns = [
    path("", include(router.urls)),
    path("bookings/", BookingListCreateView.as_view(), name="api-bookings"),
    path("bookings/<int:pk>/", BookingDetailView.as_view(), name="api-booking-detail"),
    path("cart/menu-items", cart_items, name="cart-items"),
    path("orders", OrderListCreateView.as_view(), name="orders"),
    path("orders/<int:pk>", OrderDetailView.as_view(), name="order-detail"),
    path("groups/manager/users", GroupUsersView.as_view(), {"group_name": "Manager"}, name="manager-users"),
    path("groups/delivery-crew/users", GroupUsersView.as_view(), {"group_name": "Delivery Crew"}, name="delivery-crew-users"),
]
