from flask import Flask, flash, render_template, url_for, redirect, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager, login_user, current_user, logout_user, login_required
from flask_admin import Admin
from flask_fontawesome import FontAwesome



app = Flask(__name__, template_folder='templates')
app.secret_key = 'test'
app.config.from_object('config.Config')
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'
app.config["SQLALCHEMY_DATABASE_URI"] = "postgres://hansol:9088@localhost:5432/ticketbox"
fa = FontAwesome(app)


db = SQLAlchemy(app)


migrate = Migrate(app,db)

from src.models import User, Event, Ratings, Order, OrderItems, Ticket

from src.components.user import user_blueprint
app.register_blueprint(user_blueprint, url_prefix='/user')

from src.components.event import event_blueprint
app.register_blueprint(event_blueprint, url_prefix='/event')


from src.models.admin import MyAdmin
admin = Admin(app, name='Hansol', template_mode='bootstrap3')
admin.add_view(MyAdmin(User, db.session))


login_manager = LoginManager(app)
# login_manager.init_app(app)
login_manager.login_view= 'login'



@login_manager.user_loader 
def load_user(user_id):
    return User.query.get(user_id)


@app.route('/')
def root():
    events= Event.query.all()
    return render_template('home.html', events=events)

@app.route('/login' , methods=['GET', 'POST'])
def login():
    if request.method == 'POST' :
        user = User.query.filter_by(email = request.form['email']).first()
        if current_user.is_authenticated :
            return redirect(url_for('root'))

        if not user :
            flash('Please Sign up first','warning')
            return redirect(url_for('register'))

        if user.check_password(request.form['password']):
                    login_user(user)
                    flash('Welcome! {0}'.format(user.email), 'success')
                    return redirect(url_for('root'))

        flash('Incorrect Password or Email!', 'danger')
        return redirect(url_for('signin'))

    return render_template('user/login.html')
     


@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You've successfully sign out !",'success')
    return redirect(url_for('root'))


@app.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'POST' :
        user = User.query.filter_by(email = request.form['email']).first()

        if user :
            flash('Email already taken!','warning')
            return redirect(url_for('register'))
        else : 
            user = User(email = request.form['email'], 
                        username= request.form['username'])
            user.set_password(request.form['password'])
            db.session.add(user)
            db.session.commit()
            flash("You've successfully login" , 'success')
            return redirect(url_for('login'))
    return render_template('user/register.html')