from django.contrib.contenttypes.models import ContentType

from auditlog.models import LogEntry
from auditlog.context import set_actor
from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from .models import Project
from .serializers import ProjectSerializer
from .serializers import LogEntrySerializer


class ProjectViewSet(viewsets.ModelViewSet):
    """
    Standard CRUD endpoints for the Project model.
    Only authenticated users can access.
    """

    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        with set_actor(self.request.user):
            serializer.save(created_by=self.request.user)

    def perform_update(self, serializer):
        with set_actor(self.request.user):
            serializer.save()

    def perform_destroy(self, instance):
        with set_actor(self.request.user):
            instance.delete()


class ProjectAuditLogView(generics.ListAPIView):
    """
    Endpoint to view audit logs for Project changes.
    Only Super Admins should typically see audit logs.
    """

    serializer_class = LogEntrySerializer
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get_queryset(self):
        try:
            project_content_type = ContentType.objects.get_for_model(Project)
            return (
                LogEntry.objects.filter(content_type=project_content_type)
                .select_related("actor")
                .order_by("-timestamp")
            )
        except ContentType.DoesNotExist:
            return LogEntry.objects.none()
