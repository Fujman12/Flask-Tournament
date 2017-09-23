from flask import Flask, render_template, redirect, url_for, request, flash, session, jsonify
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from forms import LoginForm, SignUpForm
from models import db, User, Judge, Captain, Organizer, Tournament
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, LoginManager, login_user, login_required, logout_user, current_user
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
import random

def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = 'Thisissecretkey!'
    #local
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://Fujman:1q2w3e@localhost:8889/newdb'
    # pythonwnyehre
    #app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://Armen:1q2w3e4r5t@Armen.mysql.pythonanywhere-services.com/Armen$newdb'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    migrate = Migrate(app, db)

    with app.app_context():
        # Extensions like Flask-SQLAlchemy now know what the "current" app
        # is while within this block. Therefore, you can now run........
        db.create_all()

    return app

app = create_app()

Bootstrap(app)
manager = Manager(app)
manager.add_command('db', MigrateCommand)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = None


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/<pk>')
@app.route('/')
def index(pk=0):
    signup_form = SignUpForm()

    current_tournament = Tournament.query.get(pk)
    judges = Judge.query.all()
    captains = Captain.query.all()
    tournaments = Tournament.query.all()

    current_captains = []
    caps = dict()

    if current_tournament:
        current_captains = current_tournament.captains.all()

        i = 1
        for captain in current_captains:
            key = "captain{}".format(i)
            caps[key] = captain
            i += 1
    print(current_captains)
    print(caps)
    return render_template('index.html', signup_form=signup_form, judges=judges,
                           captains=captains, tournaments=tournaments, current_tournament=current_tournament, caps=caps)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if check_password_hash(user.password, form.password.data):
                login_user(user, remember=form.remember_me.data)
                return redirect(url_for('index'))

        return "<h1>Invalid username or password<h1>"
        #return form.username.data + ';' + form.password.data

    return render_template('login.html', form=form)


@app.route('/signup/<role>', methods=['GET', 'POST'])
def signup(role=None):
    form = SignUpForm()

    if form.validate_on_submit():
        if role == 'organizer':
            new_user = Organizer(username=form.username.data, first_name=form.first_name.data, last_name=form.last_name.data,
                            password=generate_password_hash(form.password.data, method='sha256'), email=form.email.data)
        elif role == 'judge':
            new_user = Judge(username=form.username.data, first_name=form.first_name.data, last_name=form.last_name.data,
                        password=generate_password_hash(form.password.data, method='sha256'), email=form.email.data)
        elif role == 'captain':
            new_user = Captain(username=form.username.data, first_name=form.first_name.data, last_name=form.last_name.data,
                        password=generate_password_hash(form.password.data, method='sha256'), email=form.email.data)

        db.session.add(new_user)
        db.session.commit()
        flash('New user has been created! Try to Sign In')

        return redirect(url_for('index'))
        #return form.username.data + '  ' + form.email.data + '  ' + form.password.data + '  ' + form.first_name.data + '  ' + form.last_name.data


    return render_template('signup.html', form=form, role=role)


@app.route('/create_tournament', methods=['POST'])
def create_tournament():
    name = request.values['tournament-name']

    tournament = Tournament(organizer=current_user, name=name)

    for i in range(17):
        key = 'captain{}'.format(i)
        if key in request.values:
            if request.values[key] != '':
                id = request.values[key]
                cap = Captain.query.get(int(id))
                cap.tournament = tournament
                db.session.add(cap)
                db.session.commit()

    for i in range(6):
        key = 'judge{}'.format(i)
        if key in request.values:
            if request.values[key] != '':
                id = request.values[key]
                judge = Judge.query.get(int(id))
                tournament.judges.append(judge)
                db.session.add(tournament)
                db.session.commit()

    flash('Tournament has been created successfully!')
    return redirect(url_for('index'))


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/judges_list/<tournament_id>')
def judges_list(tournament_id):
    tournament = Tournament.query.filter_by(id=tournament_id).first()
    judges = tournament.judges.all()

    data = []

    for judge in judges:
        data.append({'name': judge.first_name + ' ' + judge.last_name, 'email': judge.email})

    print(data)
    return jsonify(data)


@app.route('/captains_list/<tournament_id>')
def captains_list(tournament_id):
    tournament = Tournament.query.filter_by(id=tournament_id).first()
    captains = tournament.captains.all()

    data = []

    for captain in captains:
        data.append({'name': captain.first_name + ' ' + captain.last_name,
                     'email': captain.email, 'team': '{} {} Team'.format(captain.first_name, captain.last_name),
                     'score': random.randint(40,90)})

    return jsonify(data)


if __name__ == '__main__':
    manager.run()


