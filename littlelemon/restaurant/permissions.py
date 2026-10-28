from rest_framework.permissions import BasePermission, SAFE_METHODS

def in_group(user, name):
    return user.is_authenticated and user.groups.filter(name=name).exists()

class IsManagerOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return request.user.is_authenticated and (request.user.is_staff or in_group(request.user, "Manager"))

class IsManager(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and (request.user.is_staff or in_group(request.user, "Manager"))

class IsCustomer(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and not request.user.is_staff and not in_group(request.user, "Manager") and not in_group(request.user, "Delivery Crew")
