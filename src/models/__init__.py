from flask_login import UserMixin, LoginManager
from src import db
import os
from werkzeug.security import generate_password_hash, check_password_hash




class User(UserMixin, db.Model) :
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False)
    avatar_url = db.Column(db.String(200),default='https://img.icons8.com/cotton/2x/person-male.png')
    email = db.Column(db.String(80), nullable=False, unique= True)
    password = db.Column(db.String(200),nullable=False)
    orders = db.relationship('Order', backref='user', lazy=True)
    admin = db.Column(db.Boolean, default=False)
    events = db.relationship('Event', backref='user', lazy=True)

    
    def set_password(self, password) :
        self.password = generate_password_hash(password)
    
    def check_password(self,password) :
        return check_password_hash(self.password, password)
    
    def is_authenticated(self):
        """Return True if the user is authenticated."""
        return self.authenticated


class Event(db.Model) :
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    title = db.Column(db.String(80), nullable=False)
    img_url = db.Column(db.String(200), default='https://i-love-png.com/images/no-image-slide.png')
    description = db.Column(db.Text)
    venue_name = db.Column(db.String(20), nullable=False)
    location = db.Column(db.String(200), nullable=False)
    time = db.Column(db.String)
    date = db.Column(db.String)
    organizer = db.Column(db.String)
    ticketss = db.relationship('Ticket', backref='event', lazy=True)
    genre = db.Column(db.String)

class Order(db.Model) :
    id = db.Column(db.Integer, primary_key=True)
    order_type = db.Column(db.String(20), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    orderitems = db.relationship('OrderItems', backref='order', lazy=True)

class Ticket(db.Model) :
    id = db.Column(db.Integer, primary_key=True)
    tic_type = db.Column(db.String(20), nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'))
    price = db.Column(db.Integer, nullable=False)
    orderitems = db.relationship('OrderItems', backref='ticket', lazy=True)
    quantity = db.Column(db.Integer, nullable=False)

class Ratings(db.Model) : # rating or like???
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'), nullable=False)
    stars = db.Column(db.Integer, nullable=False)
    user = db.relationship('User', backref='user', lazy=True)
    event = db.relationship('Event', backref='event', lazy=True)


class OrderItems(db.Model) :
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False)
    ticket_id = db.Column(db.Integer, db.ForeignKey('ticket.id'), nullable=False)
