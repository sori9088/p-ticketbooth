from flask import Blueprint, render_template

user_blueprint = Blueprint('userbp', __name__, template_folder='../../templates/user')


@user_blueprint.route('/')
def dashboard() :
    return render_template('dashboard.html')