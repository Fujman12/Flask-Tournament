from flask import Flask, render_template, redirect, url_for, request, flash, session, jsonify, render_template_string
from flask_bootstrap import Bootstrap
from flask_admin.contrib.sqla import ModelView
from forms import LoginForm, SignUpForm
from models import db, User, Judge, Captain, Organizer, Tournament, Team, Member, Pair
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, LoginManager, login_user, login_required, logout_user, current_user
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from flask_admin import Admin
from enums import positions
import random
from config import DB_PASSWORD, DB_URL, DB_USERNAME
from decimal import *


def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = 'Thisissecretkey!'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://{}:{}@{}'.format(DB_USERNAME, DB_PASSWORD, DB_URL)
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

admin = Admin(app, name='Admin Panel', template_mode='bootstrap3')
admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Captain, db.session))
admin.add_view(ModelView(Organizer, db.session))
admin.add_view(ModelView(Tournament, db.session))
admin.add_view(ModelView(Judge, db.session))
admin.add_view(ModelView(Member, db.session))


def do_something():
    print('Ok. let\'s go!')


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/<pk>')
@app.route('/')
def index(pk=0):
    signup_form = SignUpForm()

    current_tournament = Tournament.query.filter_by(id=pk).first()
    if current_tournament is None:
        current_tournament = Tournament.query.first()
        if current_tournament is None:
            current_tournament = Tournament(name='Initial')

    judges = Judge.query.all()
    captains = Captain.query.all()
    tournaments = Tournament.query.all()

    round1 = []
    round2 = []
    round3 = []
    round4 = []
    round5 = []

    for pair in current_tournament.pairs:
        if pair.round == 1:
            round1.append(pair)
        elif pair.round == 2:
            round2.append(pair)
        elif pair.round == 3:
            round3.append(pair)
        elif pair.round == 4:
            round4.append(pair)
        elif pair.round == 5:
            round5.append(pair)

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
    return render_template('index.html',
                           signup_form=signup_form,
                           judges=judges,
                           captains=captains,
                           tournaments=tournaments,
                           current_tournament=current_tournament,
                           caps=caps,
                           round1=round1,
                           round2=round2,
                           round3=round3,
                           round4=round4,
                           round5=round5,
                           positions=positions)


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
            team = Team(name='{} {} Team'.format(form.first_name.data, form.last_name.data))
            new_user = Captain(username=form.username.data, first_name=form.first_name.data, last_name=form.last_name.data,
                               password=generate_password_hash(form.password.data, method='sha256'),
                               email=form.email.data, team=team)

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
    pair = Pair(tournament=tournament)

    for i in range(17):
        key = 'captain{}'.format(i)
        if key in request.values:
            if request.values[key] != '':
                id = request.values[key]
                cap = Captain.query.get(int(id))
                cap.team.total_score = 0
                for member in cap.team.members:
                    member.score = 0
                    member.assessed = False
                    db.session.add(member)
                cap.tournament = tournament

                if len(pair.captains) < 2:
                    pair.captains.append(cap)
                else:
                    pair = Pair(tournament=tournament)
                    pair.captains.append(cap)

                db.session.add(cap)
                db.session.add(pair)
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

    number_of_teams = request.values['number-of-teams']
    tournament.number_of_teams = number_of_teams
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
                     'email': captain.email, 'team': captain.team.name,
                     'score': str(captain.team.total_score)})

    return jsonify(data)


@app.route('/all_members/<tournament_id>', methods=['GET'])
def all_members(tournament_id):
    data = []

    if current_user.role == 'organizer':
        tourn = Tournament.query.filter_by(id=tournament_id).first()
        for captain in tourn.captains:
            if captain.team:
                for member in captain.team.members:
                    data.append({'name': member.name, 'email': member.email, 'role': member.role, 'team': member.team.name,
                                 'score': str(member.score)})

        return jsonify(data)


@app.route('/remove_team/<captain_id>/', methods=['GET'])
def remove_team(captain_id):
    print(captain_id)
    captain = Captain.query.filter_by(id=captain_id).first()
    last_pair = captain.pairs[-1]
    captain.pairs.remove(last_pair)

    db.session.add(captain)
    db.session.commit()

    return jsonify({}), 200


@app.route('/advance_team/<captain_id>')
def advance_team(captain_id):
    captain = Captain.query.filter_by(id=captain_id).first()
    tournament = Tournament.query.filter_by(id=captain.tournament_id).first()
    current_pair = captain.pairs[-1]
    current_round = current_pair.round
    if current_round > 1 and len(current_pair.captains) < 2:
        return jsonify({'status': "error"})

    put = False
    for pair in tournament.pairs:
        if pair.round == current_round + 1:
            if len(pair.captains) < 2:
                put = True

                captain.team.total_score = 0
                for member in captain.team.members:
                    member.score = 0
                    member.assessed = False
                    db.session.add(member)
                    db.session.commit()
                db.session.add(captain)
                db.session.commit()

                pair.captains.append(captain)
                pair.update_scores()

                db.session.add(pair)
                db.session.commit()

    if not put:
        new_pair = Pair(tournament=tournament, round=current_round+1)
        new_pair.captains.append(captain)

        db.session.add(new_pair)
        db.session.commit()

    return jsonify({})


@app.route('/refresh_table/<tournament_pk>')
def refresh_table(tournament_pk):
    tournament = Tournament.query.filter_by(id=tournament_pk).first()
    number_of_teams = tournament.number_of_teams

    round1 = []
    round2 = []
    round3 = []
    round4 = []
    round5 = []

    for pair in tournament.pairs:
        if pair.round == 1:
            round1.append(pair)
        elif pair.round == 2:
            round2.append(pair)
        elif pair.round == 3:
            round3.append(pair)
        elif pair.round == 4:
            round4.append(pair)
        elif pair.round == 5:
            round5.append(pair)

    if number_of_teams == 16:
        return jsonify({'table_html': render_template_string('table/16.html',
                                                       round1=round1,
                                                       round2=round2,
                                                       round3=round3,
                                                       round4=round4,
                                                       round5=round5),
                        'N': number_of_teams})
    if number_of_teams == 8:
        return jsonify({'table_html': render_template('tables/8.html',
                                                       round1=round1,
                                                       round2=round2,
                                                       round3=round3,
                                                       round4=round4,
                                                       round5=round5),
                        'N': number_of_teams})

    if number_of_teams == 4:
        return jsonify({'table_html': render_template('tables/4.html',
                                                       round1=round1,
                                                       round2=round2,
                                                       round3=round3,
                                                       round4=round4,
                                                       round5=round5),
                        'N': number_of_teams})


# CAPTAIN SECTION

@app.route('/create_member', methods=['POST'])
def create_member():
    if current_user.role == 'captain':
        team = current_user.team
        name = request.values['name']
        email = request.values['email']
        role = request.values['role']
        for member in team.members:
            if member.role == role:
                return jsonify({'status': 'error'})

        member = Member(team=team, name=name, email=email, role=role)
        db.session.add(member)
        db.session.commit()

        return jsonify({'status': 'OK'})

    return jsonify({'status': 'Bad request'})


# for captain
@app.route('/members_list', methods=['GET'])
def members_list():
    data = []

    if current_user.role == 'captain':
        team = current_user.team
        members = team.members

        for member in members:
            data.append({'edit_url': url_for('edit_participant', id=member.id), 'name': member.name, 'email': member.email, 'role': member.role,
                         'score': str(member.score)})

        print(members)

        return jsonify(data)
    else:
        print('Shoit')


@app.route('/edit_participant/<id>', methods=['GET', 'POST'])
def edit_participant(id):
    if current_user.role == 'captain':
        member = Member.query.filter_by(id=id).first()
        data = dict()
        if request.method == 'GET':
            data['name'] = member.name
            data['email'] = member.email
            data['role'] = member.role

            return jsonify(data)

        else:
            name = request.values['name']
            email = request.values['email']
            role = request.values['role']

            member.name = name
            member.email = email
            member.role = role

            db.session.add(member)
            db.session.commit()

            return jsonify({'status': 'OK'})


@app.route('/edit_team_name', methods=['POST'])
def edit_team_name():
    if current_user.role == 'captain':
        team = current_user.team
        team.name = request.values['name']
        db.session.add(team)
        db.session.commit()

        return jsonify({'status': 'OK'})
    else:
        return jsonify({'status': 'Bad request'})


# JUDGE SECTION

@app.route('/judges_tournaments', methods=['GET'])
def judges_tournaments():
    if current_user.role == 'judge':

        return jsonify(tournaments=[t.serialize() for t in current_user.tournaments])


@app.route('/tournaments_teams', methods=['GET', 'POST'])
def tournaments_teams():
    if current_user.role == 'judge':
        tournament_id = request.values['id']
        tournament = Tournament.query.filter_by(id=tournament_id).first()
        teams = []
        for captain in tournament.captains:
            if captain.team:
                teams.append(captain.team)

        return jsonify(teams=[team.serialize() for team in teams])


@app.route('/tournaments_pairs', methods=['GET', 'POST'])
def tournaments_pairs():
    if current_user.role == 'judge':
        tournament_id = request.values['id']
        tournament = Tournament.query.filter_by(id=tournament_id).first()
        current_pairs = []
        for pair in tournament.pairs:
            if pair.round == tournament.current_round:
                current_pairs.append(pair)
        return jsonify(pairs=[pair.serialize() for pair in current_pairs])


@app.route('/positions_to_assess', methods=['GET', 'POST'])
def positions_to_assess():
    if current_user.role == 'judge':
        pair_id = request.values['id']
        print(pair_id)
        pair = Pair.query.filter_by(id=pair_id).first()

        positions_to_assess =[]

        for pos in positions:
            team0_position = False
            team1_position = False
            for member in pair.captains[0].team.members:
                if member.role == pos and not member.assessed:
                    team0_position = True
            for member in pair.captains[1].team.members:
                if member.role == pos and not member.assessed:
                    team1_position = True

            if team0_position and team1_position:
                positions_to_assess.append(pos)

        return jsonify(positions_to_assess=positions_to_assess)


@app.route('/select_position', methods=['GET', 'POST'])
def select_position():
    if current_user.role == 'judge':
        position = request.values['position']
        pair_id = request.values['id']
        pair = Pair.query.filter_by(id=pair_id).first()


        member0_id = None
        member1_id = None
        member0 = None
        member1 = None

        for member in pair.captains[0].team.members:
            if member.role == position:
                member0_id = member.id
                member0 = member

        for member in pair.captains[1].team.members:
            if member.role == position:
                member1_id = member.id
                member1 = member

        session['member0_id'] = member0_id
        session['member1_id'] = member1_id
        session['pair_id'] = pair.id

        return jsonify({'member0': member0.serialize(), 'member1': member1.serialize(),
                        'member0_team': member0.team.serialize(),
                        'member1_team': member1.team.serialize()})


@app.route('/teams_participants', methods=['POST'])
def teams_participants():
    if current_user.role == 'judge':
        team_id = request.values['id']
        team = Team.query.filter_by(id=team_id).first()
        if team is not None:

            return jsonify(participants=[participant.serialize() for participant in team.members])

        else:
            return jsonify(participants=[])


@app.route('/judge_select_participant', methods=['POST'])
def judge_select_participant():
    if current_user.role == 'judge':
        member_id = request.values['id']
        session['member_id'] = member_id

        return jsonify({'status': 'OK'})


@app.route('/judge_submit_score', methods=['POST'])
def judge_submit_score():
    if current_user.role == 'judge':
        total_score = 0
        values = list()
        values = request.form.getlist('value')
        team_id = request.form['team_id']
        for val in values:
            print(val)
            total_score += Decimal(val)
        member = Member.query.filter_by(team_id=team_id).first()
        member.score = total_score
        print(total_score)
        db.session.add(member)
        db.session.commit()
        member.team.count_score()
        member.team.captain.pairs[-1].update_scores()
        flash('You have successfully submitted score for {} from {}'.format(member.name, member.team.name))
    return jsonify({'score': str(total_score), 'team_score': str(member.team.total_score)})


if __name__ == '__main__':
    manager.run()


