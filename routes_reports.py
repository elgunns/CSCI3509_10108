from flask import Blueprint, jsonify

from db import connect
from fines import days_late, fine_for_days, money
from rules import balance

bp = Blueprint("reports", __name__)


@bp.route("/reports/overdue", methods=["GET"])
def report_overdue():
    conn = connect()
    rows = conn.execute(
        """
        SELECT loans.id, books.title, members.name, loans.due_date
        FROM loans
        JOIN books ON books.id = loans.book_id
        JOIN members ON members.id = loans.member_id
        WHERE loans.returned = 0
        """
    ).fetchall()
    conn.close()
    items = []
    total = 0
    for r in rows:
        days = days_late(r[3])
        if days > 0:
            fine = fine_for_days(days)
            total += fine
            items.append(
                {"loan_id": r[0], "title": r[1], "member": r[2], "days_late": days, "fine": money(fine)}
            )
    return jsonify({"items": items, "total_fines": money(total)})


@bp.route("/reports/summary", methods=["GET"])
def report_summary():
    conn = connect()
    total_books = conn.execute("SELECT COUNT(*) FROM books").fetchone()[0]
    rows = conn.execute("SELECT * FROM loans").fetchall()
    conn.close()
    outstanding, on_loan = balance(rows)
    return jsonify({"total_books": total_books, "on_loan": on_loan, "fines_outstanding": money(outstanding)})
