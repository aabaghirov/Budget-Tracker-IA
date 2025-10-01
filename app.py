from flask import Flask, render_template, request, redirect, url_for, jsonify, flash, Response
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, date
import os

app = Flask(__name__, template_folder='templates')
base_dir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(base_dir, 'budget.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = os.environ.get('SECRET_KEY', 'devkey')

db = SQLAlchemy(app)

# ---------- Models ----------
class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)

class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(200))
    amount = db.Column(db.Float, nullable=False)  # negative = expense, positive = income
    date = db.Column(db.Date, nullable=False, default=date.today)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=True)
    category = db.relationship('Category', backref=db.backref('transactions', lazy=True))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# ---------- Routes (UI) ----------

@app.route('/test2')
def test2():
    return render_template('test.html')

@app.route('/')
def index():
    income = db.session.query(db.func.sum(Transaction.amount)).filter(Transaction.amount > 0).scalar() or 0.0
    expenses = db.session.query(db.func.sum(Transaction.amount)).filter(Transaction.amount < 0).scalar() or 0.0
    recent = Transaction.query.order_by(Transaction.date.desc()).limit(10).all()
    print("DEBUG:", income, expenses, len(recent))   # <--- add this
    return render_template('index.html', income=income, expenses=expenses, recent=recent)

@app.route('/transactions')
def transactions():
    txs = Transaction.query.order_by(Transaction.date.desc()).all()
    categories = Category.query.order_by(Category.name).all()
    return render_template('transactions.html', transactions=txs, categories=categories)

@app.route('/transactions/new', methods=['GET', 'POST'])
def new_transaction():
    if request.method == 'POST':
        desc = request.form['description']
        amount = float(request.form['amount'])
        date_str = request.form.get('date') or datetime.today().strftime('%Y-%m-%d')
        dt = datetime.strptime(date_str, '%Y-%m-%d').date()
        cat_id = request.form.get('category') or None
        category = Category.query.get(cat_id) if cat_id else None
        t = Transaction(description=desc, amount=amount, date=dt, category=category)
        db.session.add(t)
        db.session.commit()
        flash('Transaction added.')
        return redirect(url_for('transactions'))
    categories = Category.query.order_by(Category.name).all()
    return render_template('transaction_form.html', categories=categories, tx=None)

@app.route('/transactions/<int:tx_id>/edit', methods=['GET', 'POST'])
def edit_transaction(tx_id):
    tx = Transaction.query.get_or_404(tx_id)
    if request.method == 'POST':
        tx.description = request.form['description']
        tx.amount = float(request.form['amount'])
        tx.date = datetime.strptime(request.form['date'], '%Y-%m-%d').date()
        cat_id = request.form.get('category') or None
        tx.category = Category.query.get(cat_id) if cat_id else None
        db.session.commit()
        flash('Transaction updated.')
        return redirect(url_for('transactions'))
    categories = Category.query.order_by(Category.name).all()
    return render_template('transaction_form.html', tx=tx, categories=categories)

@app.route('/transactions/<int:tx_id>/delete', methods=['POST'])
def delete_transaction(tx_id):
    tx = Transaction.query.get_or_404(tx_id)
    db.session.delete(tx)
    db.session.commit()
    flash('Transaction deleted.')
    return redirect(url_for('transactions'))

# ---------- Categories ----------
@app.route('/categories')
def categories_view():
    cats = Category.query.order_by(Category.name).all()
    return render_template('categories.html', categories=cats)

@app.route('/categories/add', methods=['POST'])
def add_category():
    name = request.form['name'].strip()
    if name:
        if not Category.query.filter_by(name=name).first():
            db.session.add(Category(name=name))
            db.session.commit()
            flash('Category added.')
        else:
            flash('Category already exists.')
    return redirect(url_for('categories_view'))

@app.route('/categories/<int:cat_id>/delete', methods=['POST'])
def delete_category(cat_id):
    cat = Category.query.get_or_404(cat_id)
    # remove category from its transactions
    for t in cat.transactions:
        t.category = None
    db.session.delete(cat)
    db.session.commit()
    flash('Category deleted.')
    return redirect(url_for('categories_view'))

# ---------- API: monthly summary (last 6 months) ----------
@app.route('/api/summary')
def api_summary():
    # Query aggregated sums by YYYY-MM (SQLite strftime)
    results = db.session.query(
        db.func.strftime('%Y-%m', Transaction.date).label('month'),
        db.func.sum(Transaction.amount).label('total')
    ).group_by('month').order_by('month').all()

    totals = {r.month: float(r.total or 0.0) for r in results}

    # build last 6 months labels
    today = date.today()
    def month_pair(offset):
        # offset = -5 .. 0
        y = today.year + (today.month - 1 + offset) // 12
        m = (today.month - 1 + offset) % 12 + 1
        return f"{y}-{m:02d}"

    labels = [month_pair(i) for i in range(-5, 1)]
    data = [totals.get(label, 0.0) for label in labels]
    return jsonify({"labels": labels, "data": data})

# ---------- CSV Export ----------
@app.route('/export.csv')
def export_csv():
    import csv
    from io import StringIO
    si = StringIO()
    cw = csv.writer(si)
    cw.writerow(['id', 'description', 'amount', 'date', 'category'])
    for tx in Transaction.query.order_by(Transaction.date.desc()).all():
        cw.writerow([tx.id, tx.description, tx.amount, tx.date.isoformat(), tx.category.name if tx.category else ""])
    output = si.getvalue()
    return Response(output, mimetype='text/csv', headers={"Content-Disposition": "attachment; filename=transactions.csv"})

# ---------- Helpers ----------
@app.cli.command("init-db")
def init_db():
    db.create_all()
    print("DB created (use seed_data.py to populate sample data)")

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)

