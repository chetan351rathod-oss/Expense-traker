# Expense Tracker

A web-based personal expense tracker built with Python (Flask) and SQLite. Add your daily expenses, filter them by date and category, and understand your spending through interactive charts, all in a clean dark dashboard.

## Features

- Add expenses with description, amount, date and category
- Delete expenses with one click
- Filter by start date, end date and category, with the total updating for the filtered results
- Interactive charts (built with Chart.js) that update with your filters:
  - Doughnut / pie chart: spending split by category
  - Line chart: spending over time
  - Bar chart: compare totals across categories or days
- Responsive design that works on desktop, tablet and mobile
- Local database: your data is stored in a SQLite file on your own computer

## Tech Stack

| Part | Technology |
|------|------------|
| Backend | Python, Flask |
| Database | SQLite (sqlite3 module) |
| Frontend | HTML, CSS, Jinja templates |
| Charts | Chart.js |

## Project Structure

```
expense_tracker/
├── app.py              # Flask routes and database logic
├── requirements.txt    # Python dependencies
├── templates/
│   └── index.html      # Dashboard page
└── static/
    └── style.css       # Dashboard styling
```

## How to Run

1. Clone the repository:
   ```bash
   git clone https://github.com/chetan351rathod-oss/Expense-traker.git
   cd Expense-traker
   ```
2. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Start the app:
   ```bash
   python app.py
   ```
4. Open http://127.0.0.1:5000 in your browser.

## How It Works

- `/` shows the dashboard. It reads the filters, queries the database, and calculates the total and chart data.
- `/add` saves a new expense.
- `/delete/<id>` removes an expense.

## Future Plans

- AI assistant (Claude API) to add and query expenses by chatting
- Monthly budgets with alerts
- Recurring expenses
- CSV import and export
- User login
