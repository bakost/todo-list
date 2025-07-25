from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, permissions
from .models import Todo
from .serializers import TodoSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from .tasks import export_todos_csv
from celery.result import AsyncResult

class TodoViewSet(viewsets.ModelViewSet):
    queryset = Todo.objects.all().order_by('-created_at')
    serializer_class = TodoSerializer
    permission_classes = [permissions.IsAuthenticated]

    # Enable filtering
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['status', 'priority']

    @action(detail=False, methods=['post'], url_path='export')
    def export(self, request):
        user = request.user
        task = export_todos_csv.delay(user.id)
        return Response({
            'message': 'Export task started',
            'task_id': task.id
        }, status=status.HTTP_202_ACCEPTED)
    
    @action(detail=False, methods=['get'], url_path='export/status')
    def export_status(self, request):
        task_id = request.query_params.get('task_id')
        if not task_id:
            return Response({'error': 'task_id unknown'}, status=400)
        result = AsyncResult(task_id)
        data = {'status': result.status}
        if result.successful():
            data.update(result.result)
        return Response(data)
