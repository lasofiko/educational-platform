# Запуск Django для фронтенда Eduverse
Set-Location $PSScriptRoot
Write-Host "API: http://127.0.0.1:8000/api/v1/health/"
Write-Host "Если порт 8000 занят — остановите другой процесс или: uv run python manage.py runserver 127.0.0.1:8003"
uv run python manage.py runserver 127.0.0.1:8000
