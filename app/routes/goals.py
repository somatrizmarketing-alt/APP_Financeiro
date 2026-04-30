from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from app import db
from ..models import Goal
from datetime import datetime

goals = Blueprint('goals', __name__)

@goals.route('/goals')
@login_required
def index():
    goals_list = Goal.query.filter_by(user_id=current_user.id).all()

    enriched = []
    for g in goals_list:
        progress = (g.current_amount / g.target_amount * 100) if g.target_amount else 0

        enriched.append({
            'id': g.id,
            'name': g.name,
            'target': g.target_amount,
            'current': g.current_amount,
            'progress': round(progress, 2),
            'deadline': g.deadline
        })

    return render_template('goals.html', goals=enriched)


@goals.route('/goals/add', methods=['POST'])
@login_required
def add():
    deadline = request.form.get('deadline')

    goal = Goal(
        name=request.form['name'],
        target_amount=float(request.form['target']),
        current_amount=float(request.form.get('current', 0)),
        deadline=datetime.strptime(deadline, "%Y-%m-%d") if deadline else None,
        user_id=current_user.id
    )

    db.session.add(goal)
    db.session.commit()

    return redirect(url_for('goals.index'))