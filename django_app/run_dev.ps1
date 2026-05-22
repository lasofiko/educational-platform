Set-Location $PSScriptRoot
Write-Host 'API: http://127.0.0.1:8000/api/v1/health/'
Write-Host 'If port 8000 is busy, stop the other process or run:'
Write-Host '  uv run python manage.py runserver 127.0.0.1:8003'
uv run python manage.py runserver 127.0.0.1:8000