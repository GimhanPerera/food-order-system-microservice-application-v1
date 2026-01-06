-- =========================
-- DATABASE SCHEMA
-- =========================

CREATE TABLE foods (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    price NUMERIC(10,2) NOT NULL,
    available BOOLEAN DEFAULT TRUE
);

CREATE TABLE orders (
    id SERIAL PRIMARY KEY,
    food_id INT NOT NULL,
    quantity INT NOT NULL,
    status VARCHAR(20) DEFAULT 'PENDING',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_food
        FOREIGN KEY(food_id)
        REFERENCES foods(id)
);

CREATE TABLE notification_logs (
    id SERIAL PRIMARY KEY,
    message TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- =========================
-- INITIAL FOOD DATA
-- =========================

INSERT INTO foods (name, price, available) VALUES
('Pizza Margherita', 12.00, TRUE),
('Chicken Burger', 8.50, TRUE),
('Veggie Pasta', 9.00, TRUE),
('Fried Rice', 7.00, TRUE),
('French Fries', 4.50, TRUE);

-- =========================
-- SAMPLE ORDERS (OPTIONAL)
-- =========================

INSERT INTO orders (food_id, quantity, status) VALUES
(1, 2, 'PENDING'),
(2, 1, 'COMPLETED'),
(3, 3, 'PENDING');

-- =========================
-- SAMPLE NOTIFICATION LOGS
-- =========================

INSERT INTO notification_logs (message) VALUES
('Order 2 completed. Email notification sent (mock).');

