from django.contrib.auth import get_user_model
from django.db import models
from auditlog.registry import auditlog


User = get_user_model()


class Project(models.Model):
    STATUS_CHOICES = (
        ("TODO", "To Do"),
        ("IN_PROGRESS", "In Progress"),
        ("DONE", "Done"),
    )

    title = models.CharField(max_length=255)
    description = models.TextField()
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default="TODO")

    created_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name="projects"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title


auditlog.register(Project)
