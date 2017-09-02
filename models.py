from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True)
    first_name = db.Column(db.String(40))
    last_name = db.Column(db.String(40))
    email = db.Column(db.String(40), unique=True)
    password = db.Column(db.String(80))
    role = db.Column(db.String(50))

    __mapper_args__ = {
        'polymorphic_identity': 'user',
        'polymorphic_on': role
    }

    def __repr__(self):
        return "User {}({} {})".format(self.username, self.first_name, self.last_name)


class Organizer(User):
    __tablename__ = 'organizer'
    id = db.Column(None, db.ForeignKey('user.id'), primary_key=True)

    tournaments = db.relationship('Tournament', lazy='dynamic')

    __mapper_args__ = {
        'polymorphic_identity': 'organizer'
    }

    def __repr__(self):
        return "Organizer {}({} {})".format(self.username, self.first_name, self.last_name)


class Judge(User):
    __tablename__ = 'judge'
    id = db.Column(None, db.ForeignKey('user.id'), primary_key=True)
    tournaments = db.relationship('Tournament', lazy='dynamic')

    __mapper_args__ = {
        'polymorphic_identity': 'judge'
    }

    def __repr__(self):
        return "Judge {}({} {})".format(self.username, self.first_name, self.last_name)


class Captain(User):
    __tablename__ = 'captain'
    id = db.Column(None, db.ForeignKey('user.id'), primary_key=True)
    tournament_id = db.Column(db.Integer, db.ForeignKey('tournament.id'))
    tournament = db.relationship('Tournament', foreign_keys=[tournament_id])

    __mapper_args__ = {
        'polymorphic_identity': 'captain'
    }

    # the one-to-one relation
    team = db.relationship("Team", uselist=False, backref="captain")

    def __repr__(self):
        return "Captain {}({} {})".format(self.username, self.first_name, self.last_name)


class Tournament(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    organizer_id = db.Column(db.Integer, db.ForeignKey('organizer.id'))
    organizer = db.relationship('Organizer', foreign_keys=[organizer_id])

    judge_id = db.Column(db.Integer, db.ForeignKey('judge.id'))
    judge = db.relationship('Judge', foreign_keys=[judge_id])

    captains = db.relationship('Captain', lazy='dynamic')

    def __repr__(self):
        return "Tournament {}: Organizer - {}, Judge - {}".format(self.id, self.organizer.username, self.judge.username)


class Team(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=True)
    total_score = db.Column(db.Integer)

    captain_id = db.Column(db.Integer, db.ForeignKey('captain.id'))

    def __repr__(self):
        return "Team({}) {}: Captain - {}".format(self.id, self.name, self.captain.username)

