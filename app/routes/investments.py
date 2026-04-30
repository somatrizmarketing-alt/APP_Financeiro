from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from app.models import Investment
from app import db
from app.utils import get_price

investments = Blueprint('investments', __name__)

@investments.route('/investments')
@login_required
def index():
    data = Investment.query.filter_by(user_id=current_user.id).all()

    enriched = []

    for inv in data:
        current_price = get_price(inv.symbol)

        if current_price:
            total_value = current_price * inv.quantity
            invested = inv.buy_price * inv.quantity
            profit = total_value - invested
        else:
            total_value = invested = profit = 0

        enriched.append({
            'symbol': inv.symbol,
            'quantity': inv.quantity,
            'buy_price': inv.buy_price,
            'current_price': current_price,
            'total_value': total_value,
            'profit': profit
        })

    return render_template('investments.html', investments=enriched)

@investments.route('/investments/add', methods=['POST'])
@login_required
def add():
    inv = Investment(
        symbol=request.form['symbol'],
        name=request.form['name'],
        quantity=float(request.form['quantity']),
        buy_price=float(request.form['buy_price']),
        user_id=current_user.id
    )

    db.session.add(inv)
    db.session.commit()

    return redirect(url_for('investments.index'))