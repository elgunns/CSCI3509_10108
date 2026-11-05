import sqlite3
from datetime import date, timedelta

DB_PATH = "library.db"


def connect():
    return sqlite3.connect(DB_PATH)


def init_db():
    conn = connect()
    conn.executescript(
        """
        DROP TABLE IF EXISTS books;
        DROP TABLE IF EXISTS members;
        DROP TABLE IF EXISTS loans;
        CREATE TABLE books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT, author TEXT, isbn TEXT, available INTEGER DEFAULT 1
        );
        CREATE TABLE members (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT, email TEXT UNIQUE, type TEXT
        );
        CREATE TABLE loans (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            book_id INTEGER, member_id INTEGER, due_date TEXT,
            returned INTEGER DEFAULT 0, fine REAL DEFAULT 0,
            fine_paid INTEGER DEFAULT 0, renewals INTEGER DEFAULT 0,
            checked_out TEXT
        );
        """
    )
    books = [
        ("Clean Code", "Robert C. Martin", "9780132350884", 1),
        ("The Pragmatic Programmer", "Andrew Hunt", "9780135957059", 1),
        ("Design Patterns", "Erich Gamma", "9780201633610", 1),
        ("Refactoring", "Martin Fowler", "9780134757599", 1),
        ("Code Complete", "Steve McConnell", "9780735619678", 0),
    ]
    conn.executemany("INSERT INTO books (title, author, isbn, available) VALUES (?, ?, ?, ?)", books)
    members = [
        ("Sam Rivera", "sam@campus.edu", "student"),
        ("Dr. Noor Aziz", "noor@campus.edu", "staff"),
        ("Alex Chen", "alex@campus.edu", "student"),
    ]
    conn.executemany("INSERT INTO members (name, email, type) VALUES (?, ?, ?)", members)
    today = date.today()
    conn.execute(
        "INSERT INTO loans (book_id, member_id, due_date, checked_out) VALUES (5, 3, ?, ?)",
        ((today - timedelta(days=5)).isoformat(), (today - timedelta(days=19)).isoformat()),
    )
    conn.commit()
    conn.close()
