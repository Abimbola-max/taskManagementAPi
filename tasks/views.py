from rest_framework import viewsets, permissions
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Task
from .serializers import TaskSerializer

class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['completed', 'priority']
    ordering_fields = ['due_date', 'priority', 'created_at']

    def get_queryset(self):
        user = self.request.user
        if user.is_anonymous:
            return Task.objects.none()
        queryset = Task.objects.filter(owner=user)
        due_date_after = self.request.query_params.get('due_date_after')
        due_date_before = self.request.query_params.get('due_date_before')
        if due_date_after:
            queryset = queryset.filter(due_date__gte=due_date_after)
        if due_date_before:
            queryset = queryset.filter(due_date__lte=due_date_before)
        return queryset

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    @action(detail=True, methods=['patch'], url_path='mark-completed')
    def mark_completed(self, request, pk=None):
        task = self.get_object()
        task.completed = True
        task.save()
        serializer = self.get_serializer(task)
        return Response(serializer.data)
