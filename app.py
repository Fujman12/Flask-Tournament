from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from forms import LoginForm, SignUpForm
from models import User, Judge, db, Captain
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


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/')
@login_required
def index():
    judge = Judge(username='Klips', password=generate_password_hash('blahblah', method='sha256'), first_name='Namename', last_name='Namename',
                        email='email@email.com')
    db.session.add(judge)
    db.session.commit()
    return render_template('index.html')


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

    if form.validate_on_submit():

        return '<h1>New user has been created </h1>'
        #return form.username.data + '  ' + form.email.data + '  ' + form.password.data + '  ' + form.first_name.data + '  ' + form.last_name.data

    return render_template('signup.html', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

if __name__ == '__main__':
    manager.run()
