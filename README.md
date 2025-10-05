
# Budget Tracker (Flask + SQLite)

Track your income, expenses, and financial health with a secure, multi-user budget tracker web app.

## Features
- User registration and login (each user sees only their own data)
- Add, edit, and delete transactions
- Categorize transactions
- Dashboard with income, expenses, balance, and pie chart visualization
- Export transactions to CSV
- Responsive, modern UI (Bootstrap)
- Account management (sign out, switch account)
- Pytest test suite for automated testing

## Quick Start
1. Clone the repo and open the project folder in VS Code.
2. Create and activate a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run the app:
   ```bash
   python app.py
   ```
5. Open your browser to `http://127.0.0.1:5000`

## Usage
- Register a new account
- Log in to view your dashboard
- Add categories and transactions
- View your financial summary and pie chart
- Export your data to CSV
- Sign out or switch accounts from the Account menu

## Testing
Run the test suite with:
```bash
pytest
```

## Project Structure
- `app.py` - Main Flask app
- `templates/` - HTML templates
- `static/` - CSS and static files
- `requirements.txt` - Python dependencies
- `test_app.py` - Pytest test file

## Screenshots
Add screenshots here to showcase your dashboard and features (optional).

---
Made by Alp Arslan for Individual Assignment 1
