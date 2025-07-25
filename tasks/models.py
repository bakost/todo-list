from django.db import models

class Todo(models.Model):
    PRIORITY_CHOICES = (
        ('low', 'Низкий'),
        ('medium', 'Средний'),
        ('high', 'Высокий'),
    )
    
    STATUS_CHOICES = (
        ('pending', 'Не выполнено'),
        ('done', 'Выполнено'),
    )

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    deadline = models.DateTimeField(null=True, blank=True)
    priority = models.CharField(max_length=6, choices=PRIORITY_CHOICES, default='medium')
    status = models.CharField(max_length=7, choices=STATUS_CHOICES, default='pending')

    def __str__(self):
        return self.title
