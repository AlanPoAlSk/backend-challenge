from rest_framework import serializers
from .models import Task, Label

class LabelSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Label
        fields = ['id', 'name', 'owner', 'created_at']

class TaskSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    labels = LabelSerializer(many=True, read_only=True)
    label_ids = serializers.PrimaryKeyRelatedField(queryset=Label.objects.all(), many=True, write_only=True)

    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'completed', 'owner', 'labels', 'label_ids', 'created_at', 'updated_at']