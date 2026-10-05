import os
import sqlite3
from flask import Flask, render_template, request, jsonify

BACKEND_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(BACKEND_DIR)
FRONTEND_DIR = os.path.join(PROJECT_ROOT, 'frontend')
DATABASE_DIR = os.path.join(PROJECT_ROOT, 'database')

app = Flask(
    __name__,
    template_folder=os.path.join(FRONTEND_DIR, 'templates'),
    static_folder=os.path.join(FRONTEND_DIR, 'static')
)
DB_FILE = os.path.join(DATABASE_DIR, 'grocery.db')
SCHEMA_FILE = os.path.join(DATABASE_DIR, 'schema.sql')


def get_db_connection():
    """Returns a SQLite connection with Row factory enabled."""
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db():
    """Initializes the SQLite database from schema.sql upon startup."""
    print(f"[*] Initializing database from {SCHEMA_FILE}...")
    with get_db_connection() as conn:
        with open(SCHEMA_FILE, 'r', encoding='utf-8') as f:
            conn.executescript(f.read())
        conn.commit()
    print("[+] Database initialized successfully.")


@app.route('/')
def index():
    """Serve the modern grocery store frontend with products and categories."""
    conn = get_db_connection()
    categories = conn.execute("SELECT * FROM categories ORDER BY category_id ASC").fetchall()
    products = conn.execute("""
        SELECT p.*, c.name AS category_name
        FROM products p
        JOIN categories c ON p.category_id = c.category_id
        ORDER BY p.product_id ASC
    """).fetchall()
    conn.close()
    return render_template('index.html', categories=categories, products=products)


@app.route('/database')
def database_design():
    """Serve visual database design, ERD diagram, and schema inspection."""
    conn = get_db_connection()
    tables = ['categories', 'products', 'users', 'orders', 'order_items']
    db_info = {}
    for table in tables:
        schema_row = conn.execute("SELECT sql FROM sqlite_master WHERE type='table' AND name=?", (table,)).fetchone()
        schema_sql = schema_row['sql'] if schema_row else ''
        cols = conn.execute(f"PRAGMA table_info({table})").fetchall()
        rows = conn.execute(f"SELECT * FROM {table} LIMIT 10").fetchall()
        db_info[table] = {
            'schema': schema_sql,
            'columns': [dict(c) for c in cols],
            'rows': [dict(r) for r in rows]
        }

    relational_data = conn.execute("""
        SELECT 
            o.order_id,
            u.name AS customer_name,
            p.name AS product_name,
            c.name AS category_name,
            oi.quantity,
            oi.unit_price,
            (oi.quantity * oi.unit_price) AS line_total,
            o.total_amount,
            o.status,
            o.order_date
        FROM orders o
        JOIN users u ON o.user_id = u.user_id
        JOIN order_items oi ON o.order_id = oi.order_id
        JOIN products p ON oi.product_id = p.product_id
        JOIN categories c ON p.category_id = c.category_id
        ORDER BY o.order_id DESC, oi.order_item_id ASC
    """).fetchall()

    conn.close()
    return render_template('database_design.html', db_info=db_info, relational_data=[dict(r) for r in relational_data])


@app.route('/api/products', methods=['GET'])
def get_products():
    """API endpoint to get all grocery products."""
    conn = get_db_connection()
    products = conn.execute("""
        SELECT p.*, c.name AS category_name
        FROM products p
        JOIN categories c ON p.category_id = c.category_id
        ORDER BY p.product_id ASC
    """).fetchall()
    conn.close()
    return jsonify([dict(p) for p in products])


@app.route('/api/categories', methods=['GET'])
def get_categories():
    """API endpoint to get all grocery categories."""
    conn = get_db_connection()
    categories = conn.execute("SELECT * FROM categories ORDER BY category_id ASC").fetchall()
    conn.close()
    return jsonify([dict(c) for c in categories])


@app.route('/api/orders', methods=['POST'])
def create_order():
    """API endpoint to place an order, updating 'orders' and 'order_items' tables."""
    data = request.get_json() or {}
    user_id = data.get('user_id', 1)
    total_amount = data.get('total_amount', 0.0)
    items = data.get('items', [])

    if not items:
        return jsonify({'error': 'Order must contain at least one item.'}), 400

    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO orders (user_id, total_amount, status) VALUES (?, ?, ?)",
            (user_id, total_amount, 'Confirmed')
        )
        order_id = cursor.lastrowid

        for item in items:
            product_id = item['product_id']
            quantity = item['quantity']
            unit_price = item['unit_price']
            cursor.execute(
                "INSERT INTO order_items (order_id, product_id, quantity, unit_price) VALUES (?, ?, ?, ?)",
                (order_id, product_id, quantity, unit_price)
            )

        conn.commit()
        return jsonify({
            'success': True,
            'order_id': order_id,
            'message': 'Order successfully created.'
        }), 201
    except Exception as e:
        conn.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        conn.close()


@app.route('/api/orders', methods=['GET'])
def list_orders():
    """API endpoint to list orders and verify database persistence."""
    conn = get_db_connection()
    orders = conn.execute("""
        SELECT o.*, u.name as user_name, u.email as user_email
        FROM orders o
        JOIN users u ON o.user_id = u.user_id
        ORDER BY o.order_id DESC
    """).fetchall()
    conn.close()
    return jsonify([dict(o) for o in orders])


# Initialize database automatically on startup
init_db()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
