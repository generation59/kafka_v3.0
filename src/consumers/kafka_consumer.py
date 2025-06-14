import json
import logging
from typing import Dict, Any

import yaml
from confluent_kafka import Consumer, KafkaError
from src.models.database import User, Order

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def load_config() -> Dict[str, Any]:
    """Загрузка конфигурации из YAML файла."""
    with open('src/config/config.yaml', 'r') as f:
        return yaml.safe_load(f)


def create_consumer(config: Dict[str, Any]) -> Consumer:
    """Создание Kafka consumer."""
    kafka_config = {
        'bootstrap.servers': config['kafka']['bootstrap_servers'],
        'group.id': config['kafka']['group_id'],
        'auto.offset.reset': config['kafka']['auto_offset_reset']
    }
    return Consumer(kafka_config)


def process_message(msg_value: str) -> None:
    """Обработка сообщения из Kafka."""
    try:
        data = json.loads(msg_value)
        if 'payload' not in data:
            return

        payload = data['payload']
        operation = payload.get('op')
        source = payload.get('source', {}).get('table')

        if operation == 'r':  # Read
            logger.info(f"Read operation on table {source}")
        elif operation == 'c':  # Create
            logger.info(f"Create operation on table {source}")
        elif operation == 'u':  # Update
            logger.info(f"Update operation on table {source}")
        elif operation == 'd':  # Delete
            logger.info(f"Delete operation on table {source}")

        # Преобразование данных в соответствующие модели
        if source == 'users':
            user = User.from_dict(payload['after'])
            logger.info(f"Processed user: {user}")
        elif source == 'orders':
            order = Order.from_dict(payload['after'])
            logger.info(f"Processed order: {order}")

    except json.JSONDecodeError:
        logger.error(f"Failed to decode message: {msg_value}")
    except Exception as e:
        logger.error(f"Error processing message: {e}")


def main():
    """Основная функция."""
    config = load_config()
    consumer = create_consumer(config)
    
    try:
        consumer.subscribe(config['kafka']['topics'])
        logger.info("Started consuming messages...")

        while True:
            msg = consumer.poll(1.0)
            if msg is None:
                continue
            if msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    continue
                else:
                    logger.error(f"Consumer error: {msg.error()}")
                    break

            process_message(msg.value().decode('utf-8'))

    except KeyboardInterrupt:
        logger.info("Stopping consumer...")
    finally:
        consumer.close()


if __name__ == '__main__':
    main() 