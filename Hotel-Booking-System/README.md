# Система Бронирования Отелей (Микросервисы)

Это приложение было разбито на три микросервиса:
1.  **Guest Service** (Сервис Гостей) - порт 8001
2.  **Room Service** (Сервис Комнат) - порт 8002
3.  **Booking Service** (Сервис Бронирования) - порт 8003

## Требования

- Python 3.9+
- pip

## Установка зависимостей

Перед запуском необходимо установить зависимости для всех сервисов. Вы можете сделать это одной командой:

```bash
python3 -m pip install fastapi uvicorn sqlalchemy requests pydantic
```

## Запуск микросервисов

Для удобства предусмотрен скрипт запуска, который поднимает все три сервиса одновременно:

```bash
chmod +x run_services.sh
./run_services.sh
```

Или при помощи докера
 
```bash
docker compose up --build
```

Если вы хотите запустить их вручную, выполните следующие команды в разных терминалах:

**Guest Service:**
```bash
cd services/guest_service
uvicorn src.main:app --port 8001 --reload
```

**Room Service:**
```bash
cd services/room_service
uvicorn src.main:app --port 8002 --reload
```

**Booking Service:**
```bash
cd services/booking_service
uvicorn src.main:app --port 8003 --reload
```

## Проверка работы

Вы можете запустить скрипт проверки, который протестирует полный цикл работы (создание комнаты, бронирование, проверка гостя):

```bash
python3 verify_migration.py
```

## Документация API

После запуска сервисов, интерактивная документация (Swagger UI) доступна по адресам:

- **Guest Service:** http://localhost:8001/docs
- **Room Service:** http://localhost:8002/docs
- **Booking Service:** http://localhost:8003/docs

## Запуск через Docker (Рекомендуемо)

Самый простой и надежный способ запуска — использование Docker. Это гарантирует идентичность окружения локально и на сервере.

```bash
docker-compose up --build
```
Эта команда соберет образы и запустит контейнеры.

## Развертывание на удаленном сервере

1.  **Подготовка сервера**:
    - Установите Docker и Docker Compose.
2.  **Доставка кода**:
    - Скопируйте файлы на сервер (через `git clone` или `scp`).
    ```bash
    scp -r . user@your-server-ip:/path/to/app
    ```
3.  **Запуск**:
    - Зайдите на сервер и выполните команду запуска:
    ```bash
    cd /path/to/app
    docker-compose up -d --build
    ```
    Флаг `-d` запустит сервисы в фоновом режиме.

## Тестовый запрос (CURL)

Если вы хотите проверить работу вручную из консоли:

**Создать комнату:**
```bash
curl -X 'POST' \
  'http://localhost:8002/rooms/' \
  -H 'Content-Type: application/json' \
  -d '{
  "room_type": "deluxe",
  "price": 200,
  "room_number": 505
}'
```

**Создать бронирование:**
```bash
curl -X 'POST' \
  'http://localhost:8003/bookings/' \
  -H 'Content-Type: application/json' \
  -d '{
  "check_in": "2026-06-01",
  "check_out": "2026-06-10",
  "status": "reserved",
  "guest_passport": "DEF123456",
  "room_number": 505,
  "guest_name": "Alice Smith",
  "guest_phone": "+0987654321"
}'
```
