from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from app import db
from ..models import CardTransaction
from datetime import datetime, timedelta

cards = Blueprint('cards', __name__)

# 📊 VISUALIZAR FATURA
@cards.route('/cards')
@login_required
def index():
    transactions = CardTransaction.query.filter_by(user_id=current_user.id).all()

    total_invoice = sum(t.installment_value for t in transactions)

    return render_template('cards.html', transactions=transactions, total=total_invoice)


# ➕ ADICIONAR COMPRA PARCELADA
@cards.route('/cards/add', methods=['POST'])
@login_required
def add():
    description = request.form['description']
    total = float(request.form['total'])
    installments = int(request.form['installments'])
    date = datetime.strptime(request.form['date'], "%Y-%m-%d")

    installment_value = total / installments

    # cria todas as parcelas
    for i in range(1, installments + 1):
        transaction = CardTransaction(
            description=description,
            total_amount=total,
            installments=installments,
            installment_number=i,
            installment_value=installment_value,
            purchase_date=date + timedelta(days=30 * (i - 1)),
            user_id=current_user.id
        )

        db.session.add(transaction)

    db.session.commit()

    return redirect(url_for('cards.index'))