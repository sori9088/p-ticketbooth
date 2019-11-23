from flask import Blueprint, flash, render_template, redirect, url_for, request 
from src import db

event_blueprint = Blueprint('eventbp', __name__, template_folder='../../templates/event')

from src.models import Event

@event_blueprint.route('/new', methods=['GET', 'POST'])
def new_event() :
    if request.method == 'POST':
        new_event = Event(title=request.form['title'],
                        img_url=request.form['img_url'],
                        venue_name=request.form['venue_name'],
                        location=request.form['address'],
                        date=request.values['date'],
                        time=request.values['time'],
                        organizer=request.form['organizer'],
                        description=request.form['description'])
        db.session.add(new_event)
        db.session.commit()
        return redirect(url_for('root'))
    return render_template('new_event.html')
