from django.contrib import admin
from .models import Project


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("title", "status", "created_by", "created_at")
    list_filter = ("status",)
    search_fields = ("title", "description")
    readonly_fields = ("created_at", "updated_at", "created_by")
