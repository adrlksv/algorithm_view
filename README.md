# Algorithm Visualization Tool

![Project Logo](https://via.placeholder.com/150) *(можно добавить лого позже)*

Интерактивная платформа для визуализации работы криптографических алгоритмов (AES, RSA, ECC) с пошаговыми объяснениями.

## 🌟 Особенности

- 🎨 Визуализация работы алгоритмов в реальном времени
- 🔐 Поддержка AES (128/192/256-bit), RSA (1024/2048/4096-bit) и ECC (P-256/P-384/P-521)
- 📊 Пошаговое объяснение математических операций
- 🐳 Полная Docker-поддержка
- 🚀 Готовые Makefile-команды для быстрого старта

## 🛠 Технологии

**Frontend:**
- Vue 3 + Pinia
- Tailwind CSS
- Axios

**Backend:**
- Python + FastAPI
- Cryptography (AES/RSA/ECC)
- PostgreSQL
- Alembic (миграции)

## 🚀 Быстрый старт

### Предварительные требования
- Docker + Docker Compose
- Make (опционально)

### Запуск через Makefile

```bash
# Собрать и запустить контейнеры
make app

# Остановить контейнеры
make app-down

# Просмотр логов
make app-logs

# Зайти в контейнер (для отладки)
make app-shell
```

## После запуска:
- Frontend: http://localhost:3000

- Backend (API): http://localhost:8000

- Swagger Docs: http://localhost:8000/docs

## Ручная сборка (без Makefile)
```bash
# Собрать и запустить
docker compose -f docker_compose/app.yml up --build -d

# Остановить
docker compose -f docker_compose/app.yml down
```