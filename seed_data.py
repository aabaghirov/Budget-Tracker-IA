from app import app, db, Category, Transaction
from datetime import date

def seed():
    with app.app_context():
        db.drop_all()
        db.create_all()

        # Add categories
        food = Category(name='Food')
        rent = Category(name='Rent')
        salary = Category(name='Salary')
        db.session.add_all([food, rent, salary])
        db.session.commit()

        # Add transactions
        txs = [
            Transaction(description='Grocery shopping', amount=-50, date=date(2025, 9, 25), category=food),
            Transaction(description='Monthly rent', amount=-1200, date=date(2025, 9, 1), category=rent),
            Transaction(description='Paycheck', amount=3000, date=date(2025, 9, 30), category=salary),
        ]
        db.session.add_all(txs)
        db.session.commit()
        print("Seeded DB with sample categories and transactions.")

if __name__ == '__main__':
    seed()