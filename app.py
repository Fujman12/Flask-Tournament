from flask import Flask, render_template, redirect, url_for, request, flash
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from forms import LoginForm, SignUpForm
from models import db, User, Judge, Captain, Organizer, Tournament
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, LoginManager, login_user, login_required, logout_user, current_user
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager


def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = 'Thisissecretkey!'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://Fujman:1q2w3e@localhost:8889/newdb'
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


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignUpForm()

    #username = request.form['username']
    #first_name = request.forn['first-name']
    #last_name = request.form['last-name']

    if form.validate_on_submit():
        o = Organizer(username=form.username.data, first_name=form.first_name.data, last_name=form.last_name.data,
                    password=generate_password_hash(form.password.data, method='sha256'), email=form.email.data)
        db.session.add(o)
        db.session.commit()
        flash('User successfully created! Try to Sign In')
        return redirect(url_for('index'))
        #return form.username.data + '  ' + form.email.data + '  ' + form.password.data + '  ' + form.first_name.data + '  ' + form.last_name.data

    return render_template('signup.html', form=form)


@app.route('/test', methods=['GET', 'POST'])
def test():
    name = 'name'
    if request.method == 'POST':
        if 'sdf' not in request.values:
            return 'Value is none'
        return '{}'.format(request.values[name])

    else:
        return render_template('test.html')


@app.route('/create_tournament', methods=['POST'])
def create_tournament():
    name = request.values['tournament-name']
    judge = Judge.query.get(int(request.values['judge']))

    tournament = Tournament(organizer=current_user, judge=judge, name=name)
    for i in range(17):
        key = 'captain{}'.format(i)
        if key in request.values:
            if request.values[key] != '':
                id = request.values[key]
                cap = Captain.query.get(int(id))
                cap.tournament = tournament
                db.session.add(cap)
                db.session.commit()
    flash('Tournament has been created successfully!')
    return redirect(url_for('index'))


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

if __name__ == '__main__':
    manager.run()
