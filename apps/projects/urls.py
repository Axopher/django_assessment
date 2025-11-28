from rest_framework.routers import DefaultRouter
from django.urls import path
from .views import ProjectViewSet, ProjectAuditLogView

router = DefaultRouter()
router.register(r"projects", ProjectViewSet)

urlpatterns = [
    path('audit/projects/', ProjectAuditLogView.as_view(), name='project_audit_log'),
    *router.urls
]
