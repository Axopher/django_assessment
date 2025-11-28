from django.contrib.auth import get_user_model
from rest_framework.permissions import BasePermission

User = get_user_model()


class CanCreateUser(BasePermission):
    """
    Custom permission to enforce role-based user creation rules:
    1. Super Admin: Can create users with any role/country.
    2. Country Admin: Can create Country Members ONLY for their own country.
    """

    def has_permission(self, request, view):
        # Allow reading of user list/details if authenticated
        if request.method in ("GET", "HEAD", "OPTIONS"):
            return True

        # Only check POST (creation) method rules
        if request.method != "POST":
            return True

        user = request.user
        data = request.data

        # Rule 1: Super Admin can create any user
        if user.role == User.SUPER_ADMIN:
            return True

        # Rule 2: Country Admin logic
        if user.role == User.COUNTRY_ADMIN:
            # Country Admin can only create Country Members
            if data.get("role", User.COUNTRY_MEMBER) != User.COUNTRY_MEMBER:
                return False  # Trying to create an Admin or Super Admin

            # Country Admin can only create users for their assigned country
            target_country = data.get("country")
            if not target_country or target_country != user.country:
                return False  # Trying to create a user for a different country

            return True

        # Default: Deny creation access for Country Members or unhandled roles
        return False
