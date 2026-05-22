# UGC сервис (Flask)

Сервис для отзывов и комментариев.

## Запуск

```bash
# Установить зависимости
pip install -e .

# Настроить БД
alembic upgrade head

# Запустить
python app.py