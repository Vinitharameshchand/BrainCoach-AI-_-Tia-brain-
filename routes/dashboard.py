from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from models import db, Child, Session, Exercise
from datetime import datetime

dashboard = Blueprint('dashboard', __name__)

@dashboard.route('/')
@login_required
def index():
    children = Child.query.filter_by(parent_id=current_user.id).all()
    child_ids = [c.id for c in children]
    
    # Get last 5 sessions
    recent_sessions = []
    avg_accuracy = 0
    total_sessions = 0
    accuracy_over_time = [0] * 7 # Last 7 days
    
    if child_ids:
        recent_sessions = Session.query.filter(Session.child_id.in_(child_ids)).order_by(Session.start_time.desc()).limit(5).all()
        
        # Calculate real focus score
        all_sessions = Session.query.filter(Session.child_id.in_(child_ids), Session.avg_accuracy != None).all()
        if all_sessions:
            avg_accuracy = sum(s.avg_accuracy for s in all_sessions) / len(all_sessions)
            total_sessions = len(all_sessions)
            
            # Simple dummy data for the chart if real data is sparse
            # In a real app, you'd group by day of week
            if len(all_sessions) >= 7:
                accuracy_over_time = [s.avg_accuracy for s in all_sessions[-7:]]
            else:
                # Pad with some values or just actuals
                accuracy_over_time = [s.avg_accuracy for s in all_sessions] + [0] * (7 - len(all_sessions))

    return render_template('dashboard.html', 
                           children=children, 
                           recent_sessions=recent_sessions,
                           avg_accuracy=round(avg_accuracy, 1),
                           total_sessions=total_sessions,
                           chart_data=accuracy_over_time)

@dashboard.route('/child/add', methods=['POST'])
@login_required
def add_child():
    name = request.form.get('name')
    age = request.form.get('age')
    grade = request.form.get('grade')
    
    new_child = Child(
        name=name,
        age=age,
        grade=grade,
        parent_id=current_user.id
    )
    db.session.add(new_child)
    db.session.commit()
    
    flash('Child added successfully!')
    return redirect(url_for('dashboard.index'))

@dashboard.route('/child/delete/<int:child_id>')
@login_required
def delete_child(child_id):
    child = Child.query.get_or_404(child_id)
    if child.parent_id != current_user.id:
        flash('Unauthorized action.')
        return redirect(url_for('dashboard.index'))
    
    db.session.delete(child)
    db.session.commit()
    flash('Child removed.')
    return redirect(url_for('dashboard.index'))
