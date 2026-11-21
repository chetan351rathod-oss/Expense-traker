from datetime import date
import sqlite3

from flask import Flask, render_template, request, redirect

app = Flask(__name__)
DB = "expenses.db"
CATEGORIES = ["Food", "Transport", "Shopping", "Bills", "Entertainment", "Other"]


# ---------- Database helpers ----------
def get_db():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row  # lets the HTML use e.date, e.amount, etc.
    return conn


def init_db():
    with get_db() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS expenses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT NOT NULL,
                description TEXT NOT NULL,
                category TEXT NOT NULL,
                amount REAL NOT NULL
            )
        """)


def list_expenses(start="", end="", category=""):
    query = "SELECT * FROM expenses WHERE 1=1"
    params = []
    if start:
        query += " AND date >= ?"
        params.append(start)
    if end:
        query += " AND date <= ?"
        params.append(end)
    if category:
        query += " AND category = ?"
        params.append(category)
    query += " ORDER BY date DESC, id DESC"
    with get_db() as conn:
        return conn.execute(query, params).fetchall()


# ---------- Routes ----------
@app.route("/")
def index():
    filters = {
        "start": request.args.get("start", ""),
        "end": request.args.get("end", ""),
        "category": request.args.get("category", ""),
    }
    expenses = list_expenses(**filters)

    total = sum(e["amount"] for e in expenses)

    by_category = {}
    over_time = {}
    by_month = {}
    for e in expenses:
        by_category[e["category"]] = by_category.get(e["category"], 0) + e["amount"]
        over_time[e["date"]] = over_time.get(e["date"], 0) + e["amount"]
        month = e["date"][:7]
        by_month[month] = by_month.get(month, 0) + e["amount"]
    over_time = dict(sorted(over_time.items()))  # oldest date first for the line chart
    by_month = dict(sorted(by_month.items()))
    largest_expenses = sorted(expenses, key=lambda e: e["amount"], reverse=True)[:8]

    return render_template(
        "index.html",
        expenses=expenses,
        total=total,
        categories=CATEGORIES,
        filters=filters,
        by_category=by_category,
        over_time=over_time,
        by_month=by_month,
        largest_expenses=largest_expenses,
        today=date.today().isoformat(),
    )


@app.route("/add", methods=["POST"])
def add():
    with get_db() as conn:
        conn.execute(
            "INSERT INTO expenses (date, description, category, amount) VALUES (?, ?, ?, ?)",
            (
                request.form["date"],
                request.form["description"].strip(),
                request.form["category"],
                float(request.form["amount"]),
            ),
        )
    return redirect("/")


@app.route("/delete/<int:expense_id>", methods=["POST"])
def delete(expense_id):
    with get_db() as conn:
        conn.execute("DELETE FROM expenses WHERE id = ?", (expense_id,))
    return redirect("/")


if __name__ == "__main__":
    init_db()
    app.run(debug=True)

