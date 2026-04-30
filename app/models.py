from . import db
from flask_login import UserMixin

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(200))

class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    type = db.Column(db.String(10))  # income / expense
    category = db.Column(db.String(50))
    description = db.Column(db.String(200))

    amount = db.Column(db.Float)

    payment_method = db.Column(db.String(20))  # debit / credit
    installments = db.Column(db.Integer, default=1)
    installment_number = db.Column(db.Integer, default=1)

    date = db.Column(db.Date)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class Goal(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(100))
    target_amount = db.Column(db.Float)
    current_amount = db.Column(db.Float, default=0)

    deadline = db.Column(db.Date)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class Investment(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    symbol = db.Column(db.String(20))
    name = db.Column(db.String(100))  # ex: PETR4
    type = db.Column(db.String(50))   # ação, cripto

    quantity = db.Column(db.Float)
    buy_price = db.Column(db.Float)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class CardTransaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    description = db.Column(db.String(200))
    total_amount = db.Column(db.Float)

    installments = db.Column(db.Integer)  # ex: 6x
    installment_number = db.Column(db.Integer)  # parcela atual

    installment_value = db.Column(db.Float)

    purchase_date = db.Column(db.Date)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))