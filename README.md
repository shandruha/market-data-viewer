# Realtime Market Data Viewer

Простое приложение для визуализации рыночных котировок, обновляющихся в реальном времени.

## Структура

1. БД PostgreSQL
2. Сервис, генерирующий данные - простое приложение, сохраняющее в БД новые котировки раз в секунду.
3. Сервис, визуализирующий данные - приложение на основе библиотеки Dash, демонстрирующее динамику котировок с частотой обновления в 1 сек.

## Установка

1. Установить Docker (Docker Desktop).
2. Клонировать репозиторий (допустим, в папку C:/market-data-viewer).
3. Установить пароль к БД в файле secrets/postgres-password.txt.
3. Выполнить:

```bash
docker-compose up -d
```

После установки сервис визуализации (дэшборд) будет доступен по адресу: http://127.0.0.1:8050/
