import pytest
from app import app, db, User, Transaction, Category
from flask import url_for

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client
        with app.app_context():
            db.drop_all()

def register(client, username, password):
    return client.post('/register', data={
        'username': username,
        'password': password
    }, follow_redirects=True)

def login(client, username, password):
    return client.post('/login', data={
        'username': username,
        'password': password
    }, follow_redirects=True)

def test_user_registration_and_login(client):
    rv = register(client, 'testuser', 'testpass')
    assert b'Registration successful' in rv.data or b'Please login.' in rv.data
    rv = login(client, 'testuser', 'testpass')
    assert b'Hello, testuser!' in rv.data

def test_transaction_creation(client):
    register(client, 'user2', 'pass2')
    login(client, 'user2', 'pass2')
    # Add a category first
    client.post('/categories/add', data={'name': 'TestCat'}, follow_redirects=True)
    cat = Category.query.filter_by(name='TestCat').first()
    assert cat is not None
    # Add a transaction
    rv = client.post('/transactions/new', data={
        'description': 'Test Transaction',
        'amount': '100',
        'date': '2025-10-01',
        'category': str(cat.id)
    }, follow_redirects=True)
    assert b'Transaction added.' in rv.data
    tx = Transaction.query.filter_by(description='Test Transaction').first()
    assert tx is not None
    assert tx.amount == 100
