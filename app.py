import os

from flask import Flask

from db import DB_PATH, init_db
from routes_books import bp as books_bp
from routes_loans import bp as loans_bp
from routes_members import bp as members_bp
from routes_reports import bp as reports_bp

app = Flask(__name__)
app.register_blueprint(books_bp)
app.register_blueprint(members_bp)
app.register_blueprint(loans_bp)
app.register_blueprint(reports_bp)

if not os.path.exists(DB_PATH):
    init_db()
