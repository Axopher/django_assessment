from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import RegistrationView, UserManagementViewSet

router = DefaultRouter()
router.register(r"", UserManagementViewSet, basename="user")

urlpatterns = [
    path("register/", RegistrationView.as_view(), name="user_register"),
    *router.urls,
]
