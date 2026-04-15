import sqlite3
from werkzeug.security import generate_password_hash
from datetime import datetime

DATABASE = "spendly.db"

VALID_CATEGORIES = ["Food", "Transport", "Bills", "Health", "Entertainment", "Shopping", "Other"]


def get_db():
    """Open connection to SQLite database with row_factory and foreign keys enabled."""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db():
    """Create all tables using CREATE TABLE IF NOT EXISTS."""
    conn = get_db()
    cursor = conn.cursor()

    # Create users table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            created_at TEXT
        )
    """)

    # Create expenses table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            amount REAL NOT NULL,
            category TEXT NOT NULL,
            date TEXT NOT NULL,
            description TEXT,
            created_at TEXT,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    """)

    conn.commit()
    conn.close()


def seed_db():
    """Insert sample data for development. Safe to call multiple times."""
    conn = get_db()
    cursor = conn.cursor()

    # Check if data already exists
    cursor.execute("SELECT COUNT(*) FROM users")
    if cursor.fetchone()[0] > 0:
        conn.close()
        return

    # Create demo user
    password_hash = generate_password_hash("demo123")
    cursor.execute(
        "INSERT INTO users (name, email, password_hash) VALUES (?, ?, ?)",
        ("Demo User", "demo@spendly.com", password_hash)
    )
    user_id = cursor.lastrowid

    # Get current year and month for dates
    now = datetime.now()
    current_month = now.strftime("%Y-%m")

    # Sample expenses data - 8 expenses across all categories
    expenses = [
        (user_id, 150.50, "Food", f"{current_month}-01", "Lunch at office", datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
        (user_id, 45.00, "Transport", f"{current_month}-03", "Metro card recharge", datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
        (user_id, 2500.00, "Bills", f"{current_month}-05", "Electricity bill", datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
        (user_id, 800.00, "Health", f"{current_month}-08", "Doctor consultation", datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
        (user_id, 1200.00, "Entertainment", f"{current_month}-10", "Movie tickets and dinner", datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
        (user_id, 3500.00, "Shopping", f"{current_month}-12", "New clothes", datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
        (user_id, 250.00, "Food", f"{current_month}-15", "Grocery shopping", datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
        (user_id, 500.00, "Other", f"{current_month}-18", "Miscellaneous expense", datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
    ]

    cursor.executemany(
        "INSERT INTO expenses (user_id, amount, category, date, description, created_at) VALUES (?, ?, ?, ?, ?, ?)",
        expenses
    )

    conn.commit()
    conn.close()
