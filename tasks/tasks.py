import csv
import os
from django.conf import settings
from celery import shared_task
from .models import Todo

@shared_task(bind=True)
def export_todos_csv(self, user_id):
    filename = f'todos_export_{user_id}_{self.request.id}.csv'
    filepath = os.path.join(settings.MEDIA_ROOT, 'exports', filename)
    os.makedirs(os.path.dirname(filepath), exist_ok=True)

    with open(filepath, mode='w', encoding='utf-8', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['ID', 'Title', 'Status', 'Priority', 'Deadline'])
        for todo in Todo.objects.all().order_by('-created_at'):
            writer.writerow([
                todo.id,
                todo.title,
                todo.get_status_display(),
                todo.get_priority_display(),
                todo.deadline.isoformat() if todo.deadline else '',
            ])

    return {
        'file_url': f'{settings.MEDIA_URL}exports/{filename}',
        'task_id': self.request.id,
    }
