-- Включаем расширение для CDC
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- Создаем таблицу users
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Создаем таблицу orders
CREATE TABLE IF NOT EXISTS orders (
    id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users(id),
    product_name VARCHAR(100),
    quantity INT,
    order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Добавляем тестовые данные
INSERT INTO users (name, email) VALUES 
    ('John Doe', 'john@example.com'),
    ('Jane Smith', 'jane@example.com'),
    ('Alice Johnson', 'alice@example.com'),
    ('Bob Brown', 'bob@example.com');

INSERT INTO orders (user_id, product_name, quantity) VALUES 
    (1, 'Product A', 2),
    (1, 'Product B', 1),
    (2, 'Product C', 5),
    (3, 'Product D', 3),
    (4, 'Product E', 4); 