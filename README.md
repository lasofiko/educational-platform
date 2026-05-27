# Educational Platform

Платформа для подготовки к **ЕГЭ**: курсы по предметам, дерево тем (roadmap), уроки и задачи, прогресс ученика, отзывы и комментарии (UGC), уведомления.

---

## Зачем этот проект

| Часть | Назначение |
|-------|------------|
| **Django API** (`django_app/`) | Основной бэкенд: пользователи, предметы, roadmap, уроки, задачи, квизы, прогресс, JWT |
| **UGC** (`services/ugc/`) | Микросервис на Flask: отзывы и комментарии к урокам/предметам, модерация |
| **Notifications** (`services/notifications/`) | Микросервис на FastAPI: уведомления (например, разблокировка темы) |
| **Frontend** (`frontend/`) | React + Vite: вход, регистрация, выбор курса, профиль |

**Сейчас во фронтенде есть:** `/login`, `/courses`, `/profile`.  
**Отдельной страницы дерева курса (roadmap) в UI пока нет** — дерево доступно через API `GET /api/v1/courses/roadmap/?subject_id=`.

---

## Стек

- Python **3.12+**, [uv](https://docs.astral.sh/uv/)
- Django 5 + Django REST Framework + JWT
- Flask (UGC), FastAPI (notifications)
- React 19 + Vite
- PostgreSQL (Docker / CI) 

---

## Структура репозитория

```
educational-platform/
├── django_app/          # Django: manage.py, apps accounts/courses/progress
├── frontend/            # React SPA (npm)
├── services/
│   ├── ugc/             # Flask, порт 8001
│   └── notifications/   # FastAPI, порт 8002
├── docker-compose.yml   # web + ugc + notifications + 3× Postgres
├── pyproject.toml       # зависимости; extras: dev, ugc, notifications
└── .github/workflows/   # CI: pytest на Postgres
```

---

## Быстрый старт 

Используйте порт **8003** для Django, если на **8000** уже занят другой процесс.

### 1. Зависимости Python

Из корня репозитория:

```powershell
cd educational-platform
uv sync --extra dev
```

Для работы с UGC и notifications отдельно:

```powershell
uv sync --extra dev --extra ugc --extra notifications
```

### 2. Бэкенд (Django)

Для локальной разработки используется **PostgreSQL**. Перед запуском поднимите базы данных через Docker Compose и задайте переменные окружения из `.env.example`.

```powershell
cd django_app
uv run python manage.py migrate
uv run python manage.py seed
uv run python manage.py runserver 127.0.0.1:8003
```

Проверка: http://127.0.0.1:8003/api/v1/health/ → `{"status":"ok","service":"django"}`

### 3. Фронтенд

```powershell
cd frontend
npm install
npm run dev
```

Сайт: http://localhost:3000/login

В `frontend/.env.development` должно быть:

```env
VITE_API_BASE=http://127.0.0.1:8003
```

Прокси Vite (`frontend/vite.config.js`) направляет `/api` на `http://127.0.0.1:8003`.

### 4. Порядок запуска

1. Сначала Django (терминал 1).
2. Потом `npm run dev` (терминал 2).

---

## Микросервисы отдельно

### UGC (Flask, 8001)

```powershell
# из корня, после uv sync --extra ugc
$env:JWT_SECRET="django-insecure-dev-key-change-in-production"
$env:DJANGO_BASE_URL="http://127.0.0.1:8003"
$env:UGC_DATABASE_URL="postgresql+psycopg2://postgres:postgres@127.0.0.1:5433/ugc_db"
uv run python -m services.ugc
```

Для Django при локальном UGC:

```powershell
$env:UGC_BASE_URL="http://127.0.0.1:8001"
```

Если UGC не запущен, API курсов всё равно работает — в ответах `ugc_summary` будут нулевые значения.

### Notifications (FastAPI, 8002)

```powershell
uv sync --extra notifications
uv run python -m services.notifications
```

---

## Тесты

Сбросьте переменные БД в текущей сессии PowerShell:

```powershell
Remove-Item Env:DB_NAME, Env:DB_USER, Env:DB_PASSWORD, Env:DB_HOST, Env:DB_PORT -ErrorAction SilentlyContinue
cd educational-platform
uv sync --extra dev --extra ugc --extra notifications
uv run pytest django_app/tests/ services/ugc/tests/ services/notifications/tests/ -q
```

### Как в CI (нужен Postgres на localhost:5432)

```powershell
docker compose up -d db
# создать БД test_db при первом запуске:
docker exec -it educational-platform-db psql -U postgres -c "CREATE DATABASE test_db;"

$env:DB_NAME="test_db"
$env:DB_USER="postgres"
$env:DB_PASSWORD="postgres"
$env:DB_HOST="localhost"
$env:DB_PORT="5432"
uv run python django_app/manage.py migrate
uv run pytest django_app/tests/ services/ugc/tests/ services/notifications/tests/ -q
```

CI запускается на ветках `dev` и `main`

---

## Основные API (Django)

Базовый URL: `http://127.0.0.1:8003/api/v1/` (или `8000` в Docker).

| Метод | Путь | Описание |
|-------|------|----------|
| GET | `/health/` | Проверка работы API |
| POST | `/accounts/register/` | Регистрация |
| POST | `/accounts/login/` | Вход → `access`, `refresh` |
| GET | `/accounts/me/` | Профиль (Bearer token) |
| GET | `/courses/subjects/` | Список предметов |
| GET | `/courses/roadmap/?subject_id=1` | Дерево тем |
| GET/POST | `/progress/enrollments/` | Записи на курсы |
| GET | `/courses/objects/{type}/{id}/exists/` | Проверка цели для UGC (`lesson`, `subject`) |

Авторизация: заголовок `Authorization: Bearer <access_token>`.
