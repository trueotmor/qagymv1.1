# Базовый образ Python с нужной версией (укажите вашу)
FROM python:3.12-slim

# Устанавливаем Poetry
RUN pip install poetry

# Отключаем создание виртуального окружения (в контейнере оно не нужно)
RUN poetry config virtualenvs.create false

# Копируем файлы зависимостей
COPY pyproject.toml poetry.lock* /app/

# Рабочая директория
WORKDIR /app

# Устанавливаем зависимости
RUN poetry install --no-root --no-interaction

# Копируем весь проект
COPY . /app

# Команда для запуска тестов (можно переопределить при запуске)
CMD ["poetry", "run", "pytest"]