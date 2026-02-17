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
        all_sessions = Session.query.filter(
            Session.child_id.in_(child_ids), 
            Session.avg_accuracy != None,
            Session.result_status == 'Completed'
        ).order_by(Session.start_time.desc()).all()
        
        if all_sessions:
            avg_accuracy = sum(s.avg_accuracy for s in all_sessions) / len(all_sessions)
            total_sessions = len(all_sessions)
            
            # Get last 7 sessions for chart
            last_7 = all_sessions[:7]
            last_7.reverse()  # Reverse to show oldest to newest
            
            # Ensure all values are valid numbers (not None)
            accuracy_over_time = [round(s.avg_accuracy, 1) if s.avg_accuracy else 0 for s in last_7]
            
            # Pad with zeros if less than 7 sessions
            while len(accuracy_over_time) < 7:
                accuracy_over_time.insert(0, 0)
        else:
            # No completed sessions yet - show empty chart
            accuracy_over_time = [0, 0, 0, 0, 0, 0, 0]

    return render_template('dashboard.html', 
                           children=children, 
                           recent_sessions=recent_sessions,
                           avg_accuracy=round(avg_accuracy, 1),
                           total_sessions=total_sessions,
                           chart_data=accuracy_over_time)

@dashboard.route('/child/add', methods=['POST'])
@login_required
def add_child():
    name = request.form.get('name', '').strip()
    age = request.form.get('age', '').strip()
    grade = request.form.get('grade', '').strip()
    
    # Validation
    if not name or len(name) < 2:
        flash('Child name must be at least 2 characters long.')
        return redirect(url_for('dashboard.index'))
    
    if len(name) > 100:
        flash('Child name is too long (max 100 characters).')
        return redirect(url_for('dashboard.index'))
    
    try:
        age_int = int(age) if age else None
        if age_int and (age_int < 3 or age_int > 18):
            flash('Age must be between 3 and 18.')
            return redirect(url_for('dashboard.index'))
    except ValueError:
        flash('Invalid age value.')
        return redirect(url_for('dashboard.index'))
    
    if grade and len(grade) > 20:
        flash('Grade is too long (max 20 characters).')
        return redirect(url_for('dashboard.index'))
    
    new_child = Child(
        name=name,
        age=age_int,
        grade=grade if grade else None,
        parent_id=current_user.id
    )
    db.session.add(new_child)
    db.session.commit()
    
    flash(f'{name} has been added successfully! 🎉')
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
