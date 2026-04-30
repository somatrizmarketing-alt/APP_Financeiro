from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from app import db
from ..models import Transaction
from datetime import datetime

transactions = Blueprint('transactions', __name__)

# 📊 LISTAR
@transactions.route('/transactions')
@login_required
def index():
    data = Transaction.query.filter_by(user_id=current_user.id)\
        .order_by(Transaction.date.desc()).all()

    return render_template('transactions.html', transactions=data)


# ➕ ADICIONAR
@transactions.route('/transactions/add', methods=['POST'])
@login_required
def add():
    transaction = Transaction(
        type=request.form['type'],
        category=request.form['category'],
        description=request.form.get('description', ''),
        amount=float(request.form['amount']),
        date=datetime.strptime(request.form['date'], "%Y-%m-%d"),
        user_id=current_user.id
    )

    db.session.add(transaction)
    db.session.commit()

    return redirect(url_for('transactions.index'))


# 🗑️ DELETAR
@transactions.route('/transactions/delete/<int:id>')
@login_required
def delete(id):
    t = Transaction.query.get_or_404(id)

    if t.user_id != current_user.id:
        return "Acesso negado", 403

    db.session.delete(t)
    db.session.commit()

    return redirect(url_for('transactions.index'))