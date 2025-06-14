# Проект CDC с использованием Kafka и Debezium

Этот проект демонстрирует использование Change Data Capture (CDC) с использованием Apache Kafka, Debezium и PostgreSQL.

## Структура проекта

```
.
├── infra/
│   └── docker-compose/
│       └── docker-compose.yaml
├── src/
│   ├── config/
│   │   └── config.yaml
│   ├── models/
│   │   └── database.py
│   └── consumers/
│       └── kafka_consumer.py
└── README.md
```

## Компоненты системы

- **Apache Kafka**: Брокер сообщений для обработки потоков данных
- **Kafka Connect**: Фреймворк для подключения Kafka к внешним системам
- **PostgreSQL**: Исходная база данных с поддержкой CDC
- **Debezium**: Платформа CDC для отслеживания изменений в базе данных
- **Prometheus**: Сбор метрик
- **Grafana**: Визуализация метрик

## Требования

- Docker
- Docker Compose
- Python 3.8+

## Установка и запуск

1. Запуск инфраструктуры:
```bash
cd infra/docker-compose
docker-compose up -d
```

2. Подождите запуска всех сервисов (примерно 30-60 секунд)

3. Создание таблиц в базе данных:
```bash
docker-compose exec postgres psql -U postgres -d postgres -f /docker-entrypoint-initdb.d/init.sql
```

4. Настройка Debezium коннектора:
```bash
curl -X POST -H "Content-Type: application/json" --data @debezium-config.json http://localhost:8083/connectors
```

5. Запуск Kafka consumer:
```bash
python src/consumers/kafka_consumer.py
```

## Тестирование

1. Добавление тестовых данных в PostgreSQL:
```sql
-- Добавление пользователей
INSERT INTO users (name, email) VALUES ('John Doe', 'john@example.com');
INSERT INTO users (name, email) VALUES ('Jane Smith', 'jane@example.com');

-- Добавление заказов
INSERT INTO orders (user_id, product_name, quantity) VALUES (1, 'Product A', 2);
INSERT INTO orders (user_id, product_name, quantity) VALUES (2, 'Product B', 1);
```

2. Мониторинг вывода Kafka consumer для просмотра захваченных изменений

## Мониторинг

- Метрики Prometheus доступны по адресу: http://localhost:9090
- Дашборд Grafana доступен по адресу: http://localhost:3000

## Конфигурация

- Kafka bootstrap servers: localhost:9092
- PostgreSQL: localhost:5432
- Kafka Connect: localhost:8083
- Prometheus: localhost:9090
- Grafana: localhost:3000

## Описание компонентов

### Apache Kafka
Брокер сообщений, который обрабатывает и хранит потоки данных. В данном проекте используется для передачи изменений из базы данных.

### Kafka Connect
Фреймворк для подключения Kafka к внешним системам. В нашем случае используется для интеграции с PostgreSQL через Debezium.

### PostgreSQL
База данных, в которой хранятся исходные данные. Настроена для работы с CDC через Debezium.

### Debezium
Платформа CDC, которая отслеживает изменения в базе данных и отправляет их в Kafka. В проекте настроена для отслеживания изменений в таблицах users и orders.

### Prometheus
Система мониторинга, которая собирает метрики о работе Kafka Connect и других компонентов.

### Grafana
Инструмент визуализации, который отображает метрики, собранные Prometheus, в виде графиков и дашбордов.

## Проверка работоспособности

1. Проверка статуса коннектора:
```bash
curl -s localhost:8083/connectors/postgres-connector/status | jq
```

2. Проверка топиков Kafka:
```bash
docker-compose exec kafka kafka-topics --list --bootstrap-server kafka:29092
```

3. Проверка метрик в Prometheus:
- Откройте http://localhost:9090
- Перейдите в раздел Status -> Targets
- Убедитесь, что все цели доступны

4. Проверка дашбордов в Grafana:
- Откройте http://localhost:3000
- Войдите с учетными данными (admin/admin)
- Проверьте доступные дашборды 