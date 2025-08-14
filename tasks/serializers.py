from datetime import date

from rest_framework import serializers

from tasks.models import Task


class TaskSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Task
        fields = '__all__'
        read_only_fields = ['id', 'owner', 'created_at', 'updated_at']

    def validate_title(self, value):
        if not value.strip():
            raise serializers.ValidationError("Title cannot be empty.")
        return value

    def validate_due_date(self, value):
        if value < date.today():
            raise serializers.ValidationError("Due date cannot be in the past.")
        return value
