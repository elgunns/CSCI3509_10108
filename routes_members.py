from flask import Blueprint, jsonify, request

from db import connect
from fines import days_late, money
from rules import balance, loan_limit
from validation import check

bp = Blueprint("members", __name__)


def member_json(r):
    return {"id": r[0], "name": r[1], "email": r[2], "type": r[3]}


@bp.route("/members", methods=["GET"])
def list_members():
    conn = connect()
    rows = conn.execute("SELECT * FROM members").fetchall()
    conn.close()
    return jsonify([member_json(r) for r in rows])


@bp.route("/members/<int:member_id>", methods=["GET"])
def get_member(member_id):
    conn = connect()
    r = conn.execute("SELECT * FROM members WHERE id = ?", (member_id,)).fetchone()
    conn.close()
    if r is None:
        return jsonify({"error": "member not found"}), 404
    return jsonify(member_json(r))


@bp.route("/members", methods=["POST"])
def create_member():
    data = request.get_json(silent=True) or {}
    if not data.get("name"):
        return jsonify({"error": "name is required"}), 400
    if not check(data.get("email"), "email"):
        return jsonify({"error": "invalid email"}), 400
    member_type = data.get("type", "student")
    if not check(member_type, "member_type"):
        return jsonify({"error": "type must be student or staff"}), 400
    conn = connect()
    existing = conn.execute("SELECT * FROM members WHERE email = ?", (data["email"],)).fetchone()
    if existing is not None:
        conn.close()
        return jsonify({"error": "email already registered"}), 409
    cur = conn.execute(
        "INSERT INTO members (name, email, type) VALUES (?, ?, ?)",
        (data["name"], data["email"], member_type),
    )
    conn.commit()
    r = conn.execute("SELECT * FROM members WHERE id = ?", (cur.lastrowid,)).fetchone()
    conn.close()
    return jsonify(member_json(r)), 201


@bp.route("/members/<int:member_id>/loans", methods=["GET"])
def member_loans(member_id):
    conn = connect()
    m = conn.execute("SELECT * FROM members WHERE id = ?", (member_id,)).fetchone()
    if m is None:
        conn.close()
        return jsonify({"error": "member not found"}), 404
    rows = conn.execute("SELECT * FROM loans WHERE member_id = ?", (member_id,)).fetchall()
    conn.close()
    owed, open_loans = balance(rows)
    loans = [
        {
            "id": loan[0],
            "book_id": loan[1],
            "due_date": loan[3],
            "returned": bool(loan[4]),
            "fine": money(loan[5]),
            "fine_paid": bool(loan[6]),
        }
        for loan in rows
    ]
    remaining = loan_limit(m[3]) - open_loans
    return jsonify({"loans": loans, "total_owed": money(owed), "loans_remaining": remaining})
