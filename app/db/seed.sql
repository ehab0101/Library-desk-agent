
-- BOOKS (10)

INSERT INTO books (isbn, title, author, price, stock) VALUES
('9780132350884', 'Clean Code', 'Robert C. Martin', 35.00, 12),
('9780201616224', 'The Pragmatic Programmer', 'Andrew Hunt', 40.00, 8),
('9780134494166', 'Effective Java', 'Joshua Bloch', 45.00, 6),
('9781491957660', 'Designing Data-Intensive Applications', 'Martin Kleppmann', 50.00, 5),
('9780596007126', 'Head First Design Patterns', 'Eric Freeman', 30.00, 10),
('9780131103627', 'The C Programming Language', 'Kernighan & Ritchie', 25.00, 4),
('9780321125217', 'Domain-Driven Design', 'Eric Evans', 55.00, 3),
('9780134685991', 'Effective Modern C++', 'Scott Meyers', 48.00, 7),
('9781492078005', 'Fluent Python', 'Luciano Ramalho', 60.00, 6),
('9781617296086', 'Spring in Action', 'Craig Walls', 42.00, 5);


-- CUSTOMERS (6)

INSERT INTO customers (id, name, email) VALUES
(1, 'Alice', 'alice@example.com'),
(2, 'Bob', 'bob@example.com'),
(3, 'Charlie', 'charlie@example.com'),
(4, 'Dina', 'dina@example.com'),
(5, 'Ehab', 'ehab@example.com'),
(6, 'Faris', 'faris@example.com');


-- ORDERS (4)

INSERT INTO orders (id, customer_id) VALUES
(1, 2),
(2, 3),
(3, 1),
(4, 5);


-- ORDER ITEMS

INSERT INTO order_items (order_id, isbn, qty) VALUES
(1, '9780132350884', 1),
(1, '9780201616224', 2),
(2, '9780134494166', 1),
(3, '9780596007126', 3),
(4, '9781491957660', 1);
