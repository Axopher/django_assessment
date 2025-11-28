from django.utils.timesince import timesince
from django.utils import timezone

from auditlog.models import LogEntry
from rest_framework import serializers

from .models import Project


class ProjectSerializer(serializers.ModelSerializer):
    created_by_username = serializers.ReadOnlyField(source="created_by.username")

    class Meta:
        model = Project
        fields = [
            "id",
            "title",
            "description",
            "status",
            "created_by",
            "created_by_username",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["created_by", "created_at", "updated_at"]


class LogEntrySerializer(serializers.ModelSerializer):
    actor_username = serializers.ReadOnlyField(source="actor.username")
    actor_email = serializers.ReadOnlyField(source="actor.email")
    content_type_name = serializers.SerializerMethodField()
    action_label = serializers.SerializerMethodField()
    time_since = serializers.SerializerMethodField()
    timestamp_human = serializers.SerializerMethodField()

    class Meta:
        model = LogEntry
        fields = [
            "id",
            "timestamp",
            "timestamp_human",
            "time_since",
            "action",
            "action_label",
            "changes",
            "actor_username",
            "actor_email",
            "remote_addr",
            "content_type_name",
            "object_repr",
        ]

    def get_action_label(self, obj):
        return obj.get_action_display()

    def get_content_type_name(self, obj):
        return obj.content_type.model

    def get_time_since(self, obj):
        return timesince(obj.timestamp, timezone.now()) + " ago"

    def get_timestamp_human(self, obj):
        return obj.timestamp.strftime("%b %d, %Y, %I:%M %p")
