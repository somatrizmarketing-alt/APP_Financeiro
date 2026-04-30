from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from app.models import Transaction
from app import db
from sqlalchemy import func
from datetime import datetime


dashboard = Blueprint('dashboard', __name__)

@dashboard.route('/dashboard')
@login_required
def home():
    transactions = Transaction.query.filter_by(user_id=current_user.id).all()
    # KPIs
    income = sum(t.amount for t in transactions if t.type == 'income')
    expenses = sum(t.amount for t in transactions if t.type == 'expense')
    balance = income - expenses

    # GASTOS POR CATEGORIA
    category_data = db.session.query(
        Transaction.category,
        func.sum(Transaction.amount)
    ).filter_by(user_id=current_user.id).group_by(Transaction.category).all()

    labels = [c[0] for c in category_data]
    values = [float(c[1]) for c in category_data]

    # EVOLUÇÃO MENSAL
    monthly_data = db.session.query(
        func.strftime('%Y-%m', Transaction.date),
        func.sum(Transaction.amount)
    ).filter_by(user_id=current_user.id).group_by(func.strftime('%Y-%m', Transaction.date)).all()

    months = [m[0] for m in monthly_data]
    totals = [float(m[1]) for m in monthly_data]

    return render_template(
        'dashboard.html',
        income=income,
        expenses=expenses,
        balance=balance,
        labels=labels,
        values=values,
        months=months,
        totals=totals,
        transactions=transactions[-5:]  # últimos 5
    )


@dashboard.route('/add', methods=['POST'])
@login_required
def add():
    t = Transaction(
        type=request.form['type'],
        category=request.form['category'],
        amount=float(request.form['amount']),
        user_id=current_user.id
    )

    db.session.add(t)
    db.session.commit()

    return redirect(url_for('dashboard.home'))