-- ============================================================
-- Online Grocery Store Database Schema (SQLite)
-- ============================================================

-- 1. Categories Table
CREATE TABLE IF NOT EXISTS categories (
    category_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE
);

-- 2. Products Table
CREATE TABLE IF NOT EXISTS products (
    product_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    category_id INTEGER NOT NULL,
    price REAL NOT NULL,
    unit TEXT NOT NULL,
    stock_quantity INTEGER NOT NULL DEFAULT 0,
    image_url TEXT,
    badge TEXT DEFAULT 'Fresh',
    FOREIGN KEY (category_id) REFERENCES categories (category_id) ON DELETE CASCADE
);

-- 3. Users Table
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    address TEXT NOT NULL
);

-- 4. Orders Table
CREATE TABLE IF NOT EXISTS orders (
    order_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    total_amount REAL NOT NULL,
    status TEXT NOT NULL DEFAULT 'Pending',
    FOREIGN KEY (user_id) REFERENCES users (user_id) ON DELETE CASCADE
);

-- 5. Order Items Table
CREATE TABLE IF NOT EXISTS order_items (
    order_item_id INTEGER PRIMARY KEY AUTOINCREMENT,
    order_id INTEGER NOT NULL,
    product_id INTEGER NOT NULL,
    quantity INTEGER NOT NULL,
    unit_price REAL NOT NULL,
    FOREIGN KEY (order_id) REFERENCES orders (order_id) ON DELETE CASCADE,
    FOREIGN KEY (product_id) REFERENCES products (product_id) ON DELETE RESTRICT
);

-- Sample Data Seeding for Immediate Use (Prices in Indian Rupees - INR ₹)
INSERT OR IGNORE INTO categories (category_id, name) VALUES 
(1, 'Fresh Fruits'),
(2, 'Dairy & Eggs'),
(3, 'Bakery'),
(4, 'Vegetables'),
(5, 'Beverages & Pantry');

INSERT OR IGNORE INTO products (product_id, name, category_id, price, unit, stock_quantity, image_url, badge) VALUES
(1, 'Fresh Red Apples', 1, 149.00, '1 kg', 45, 'https://images.unsplash.com/photo-1560806887-1e4cd0b6cbd6?auto=format&fit=crop&w=600&q=80', 'Fresh'),
(2, 'Organic Whole Milk', 2, 68.00, '1 Litre', 30, 'https://images.unsplash.com/photo-1550583724-b2692b85b150?auto=format&fit=crop&w=600&q=80', 'Organic'),
(3, 'Whole Grain Artisan Bread', 3, 55.00, '400g Loaf', 25, 'https://images.unsplash.com/photo-1509440159596-0249088772ff?auto=format&fit=crop&w=600&q=80', 'Freshly Baked'),
(4, 'Organic Hass Avocados', 1, 199.00, 'Pack of 3', 35, 'https://images.unsplash.com/photo-1523049673857-eb18f1d7b578?auto=format&fit=crop&w=600&q=80', 'Organic'),
(5, 'Crisp Baby Spinach', 4, 39.00, '250g Bunch', 40, 'https://images.unsplash.com/photo-1576045057995-568f588f82fb?auto=format&fit=crop&w=600&q=80', 'Farm Fresh'),
(6, 'Farm Fresh Brown Eggs', 2, 85.00, 'Pack of 6', 50, 'https://images.unsplash.com/photo-1582722872445-44dc5f7e3c8f?auto=format&fit=crop&w=600&q=80', 'Organic'),
(7, 'Sweet Cluster Tomatoes', 4, 45.00, '1 kg', 38, 'https://images.unsplash.com/photo-1546094096-0df4bcaaa337?auto=format&fit=crop&w=600&q=80', 'Fresh'),
(8, 'Golden Raw Wildflower Honey', 5, 299.00, '350g Jar', 20, 'https://images.unsplash.com/photo-1587049352846-4a222e784d38?auto=format&fit=crop&w=600&q=80', 'Natural');

INSERT OR IGNORE INTO users (user_id, name, email, address) VALUES
(1, 'Aarav Sharma', 'aarav.sharma@example.com', 'Flat 402, Green Glen Layout, Bellandur, Bengaluru');

-- Sample Initial Verified Order in Rupees
INSERT OR IGNORE INTO orders (order_id, user_id, order_date, total_amount, status) VALUES
(1, 1, '2026-09-22 21:30:00', 384.30, 'Confirmed');

INSERT OR IGNORE INTO order_items (order_item_id, order_id, product_id, quantity, unit_price) VALUES
(1, 1, 1, 2, 149.00),
(2, 1, 2, 1, 68.00);

