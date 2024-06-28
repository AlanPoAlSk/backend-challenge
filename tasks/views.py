from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Task, Label
from .serializers import TaskSerializer, LabelSerializer
from django_filters.rest_framework import DjangoFilterBackend


class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user
    
class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['completed', 'labels']

    def get_queryset(self):
        return Task.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    @action(detail=True, methods=['post'])
    def add_label(self, request, pk=None):
        task = self.get_object()
        label_id = request.data.get('label_id')
        if label_id:
            label = Label.objects.filter(owner=request.user, id=label_id).first()
            if label:
                task.labels.add(label)
                serializer = self.get_serializer(task)
                return Response(serializer.data)
            return Response({'detail': 'Label not found or does not belong to the current user.'}, status=400)
        return Response({'detail': 'Label ID is required.'}, status=400)

    @action(detail=True, methods=['post'])
    def remove_label(self, request, pk=None):
        task = self.get_object()
        label_id = request.data.get('label_id')
        if label_id:
            label = Label.objects.filter(owner=request.user, id=label_id).first()
            if label and label in task.labels.all():
                task.labels.remove(label)
                serializer = self.get_serializer(task)
                return Response(serializer.data)
            return Response({'detail': 'Label not found or is not associated with this task.'}, status=400)
        return Response({'detail': 'Label ID is required.'}, status=400)

class LabelViewSet(viewsets.ModelViewSet):
    serializer_class = LabelSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def get_queryset(self):
        return Label.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


    def perform_update(self, serializer):
        # Ensure owner is not changed on update
        instance = serializer.save()
        if 'owner' in serializer.validated_data:
            instance.owner = self.request.user
            instance.save()

