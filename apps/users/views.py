from django.contrib.auth import get_user_model

from rest_framework import generics, viewsets
from rest_framework.permissions import IsAuthenticated

from .permissions import CanCreateUser
from .serializers import UserRegistrationSerializer

User = get_user_model()


class RegistrationView(generics.CreateAPIView):
    """
    Endpoint for user registration, restricted by custom role-based permission.
    """

    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [IsAuthenticated, CanCreateUser]


class UserManagementViewSet(viewsets.ModelViewSet):
    """
    Allows Super Admins to view/edit all users and Country Admins to view users in their country.
    """

    queryset = User.objects.all().order_by("id")
    serializer_class = UserRegistrationSerializer
    permission_classes = [IsAuthenticated, CanCreateUser]

    def get_queryset(self):
        user = self.request.user

        if user.role == User.SUPER_ADMIN:
            return User.objects.all()

        if user.role == User.COUNTRY_ADMIN:
            # Country Admin can only see users in their assigned country
            return User.objects.filter(country=user.country)

        # Country Members can only see their own profile
        return User.objects.filter(id=user.id)
