# Todo List API

REST API для управления списком задач (To-do list), с возможностью асинхронного экспорта данных.  

---

## Функции

- Полный CRUD (создание, чтение, обновление, удаление) задач  
- Аутентификация через JWT (SimpleJWT)  
- Фильтрация по статусу и приоритету (django-filter)  
- Асинхронный экспорт задач в CSV через Celery + Redis  
- Проверка статуса задачи экспорта и скачивание готового файла  

---

## Технологии

- Python 3.12  
- Django 5.2  
- Django REST Framework  
- djangorestframework-simplejwt  
- django-filter  
- Celery  
- Redis  

---

## Быстрый старт

1. Клонировать репозиторий  
   ```bash
   git clone https://github.com/bakost/todo-list.git
   cd todo-list
   ```

2. Создать виртуальное окружение и установить зависимости  
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```

3. Настроить .env (например)
   ```
   SECRET_KEY=<ваш_secret_key>
   DEBUG=True
   CELERY_BROKER_URL=redis://localhost:6379/0
   CELERY_RESULT_BACKEND=redis://localhost:6379/1
   DATABASE_URL=postgres://<user>:<password>@localhost:5432/<dbname>
   ```

4. Применить миграции  
   ```bash
   python manage.py migrate
   ```

5. Создать суперпользователя  
   ```bash
   python manage.py createsuperuser
   ```

6. Запустить Redis (локально или в Docker)  
   ```bash
   # локально, если установлен:
   redis-server --daemonize yes

   # или Docker:
   docker run -d --name redis -p 6379:6379 redis:latest
   ```

7. Поднять Celery-воркер  
   ```bash
   celery -A todo_list worker -l info
   ```

8. Запустить Django-сервер  
   ```bash
   python manage.py runserver
   ```

---

## Описание решения

1. **DRF и CRUD**  
   - `TodoViewSet` на `ModelViewSet` обеспечивает стандартные методы:  
     - `GET /api/todos/` — список  
     - `GET /api/todos/{id}/` — детали  
     - `POST /api/todos/` — создание  
     - `PUT/PATCH /api/todos/{id}/` — обновление  
     - `DELETE /api/todos/{id}/` — удаление  

2. **JWT-аутентификация**  
   - Эндпоинты:  
     - `POST /api/token/` — получение `access` и `refresh`  
     - `POST /api/token/refresh/` — обновление `access`  
   - Все `/api/todos/` защищены `IsAuthenticated`

3. **Фильтрация**  
   - Подключён `django_filters.rest_framework.DjangoFilterBackend`  
   - Параметры запроса: `?status=…&priority=…`

4. **Асинхронный экспорт**  
   - Celery-таск `export_todos_csv`, сохраняет CSV в `MEDIA_ROOT/exports`  
   - Кастомный экшен `POST /api/todos/export/` запускает экспорт  
   - `GET /api/todos/export/status/?task_id={id}` возвращает статус, `file_url`, ошибку или traceback  

---

## Примеры запросов

1. Получить токены:
   ```bash
   curl -X POST http://127.0.0.1:8000/api/token/ \
     -H "Content-Type: application/json" \
     -d '{"username":"admin","password":"pass"}'
   ```

2. Создать задачу:
   ```bash
   curl -X POST http://127.0.0.1:8000/api/todos/ \
     -H "Authorization: Bearer <access_token>" \
     -H "Content-Type: application/json" \
     -d '{"title":"Task","description":"Desc","deadline":"2025-08-01T12:00:00Z","priority":"low"}'
   ```

3. Фильтрация:
   ```bash
   GET /api/todos/?status=pending&priority=high
   ```

4. Запуск экспорта:
   ```bash
   POST /api/todos/export/ \
     -H "Authorization: Bearer <access_token>"
   ```

5. Проверка статуса:
   ```bash
   GET /api/todos/export/status/?task_id=<task_id> \
     -H "Authorization: Bearer <access_token>"
   ```
