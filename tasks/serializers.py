from rest_framework import serializers
from .models import Todo

class TodoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Todo
        fields = [
            'id',
            'title',
            'description',
            'created_at',
            'deadline',
            'priority',
            'status',
        ]
        read_only_fields = ['id', 'created_at']
