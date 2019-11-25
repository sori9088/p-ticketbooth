from flask import Blueprint, flash, render_template, redirect, url_for, request 
from src import db
from sqlalchemy import func
from flask_login import LoginManager, login_user, current_user, logout_user, login_required

event_blueprint = Blueprint('eventbp', __name__, template_folder='../../templates/event')

from src.models import Event, Ticket

@event_blueprint.route('/new', methods=['GET', 'POST'])
def new_event() :
    if request.method == 'POST':
        new_event = Event(title=request.form['title'],
                        user_id=current_user.id,
                        img_url=request.form['img_url'],
                        venue_name=request.form['venue_name'],
                        location=request.form['address'],
                        date=request.values['date'],
                        time=request.values['time'],
                        organizer=request.form['organizer'],
                        description=request.form['description'])
        db.session.add(new_event)
        new_ticket = Ticket(tic_type= request.form['tic_type'],
                            price=request.form['price'],
                            quantity=request.form['quantity'])
        db.session.add(new_ticket)
        db.session.commit()
        event= Event.query.filter_by(title=request.form['title']).first()
        ticket= Ticket.query.filter_by(tic_type= request.form['tic_type']).first()
        event.ticketss.append(ticket)
        db.session.commit()

        return redirect(url_for('root'))
    return render_template('new_event.html')


@event_blueprint.route('/<id>', methods=['GET','POST'])
def singleevent(id):
    single = Event.query.filter_by(id = id).first()
    return render_template('single_event.html',single=single)