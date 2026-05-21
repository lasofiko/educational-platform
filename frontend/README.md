# Eduverse Frontend

Экран авторизации (Log in / Sign up) без соцкнопок.

## Запуск

```bash
cd frontend
npm install
npm run dev
```

Открой http://localhost:3000

| Страница | URL |
|----------|-----|
| Вход / регистрация | `/login` |
| Выбор курса | `/courses` (после входа) |

Django API: `http://127.0.0.1:8000` (см. `.env.development`). Запусти бэкенд:

```powershell
cd django_app
uv run python manage.py runserver
```

Если видишь **Not found** при регистрации — Django не запущен или запрос не доходит до порта 8000.

## Сборка

```bash
npm run build
```
