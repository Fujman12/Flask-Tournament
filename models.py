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


class Organizer(User):
    __tablename__ = 'organizer'
    id = db.Column(None, db.ForeignKey('user.id'), primary_key=True)

    tournaments = db.relationship('Tournament', lazy='dynamic')

    __mapper_args__ = {
        'polymorphic_identity': 'organizer'
    }


class Judge(User):
    __tablename__ = 'judge'
    id = db.Column(None, db.ForeignKey('user.id'), primary_key=True)
    tournaments = db.relationship('Tournament', lazy='dynamic')

    __mapper_args__ = {
        'polymorphic_identity': 'judge'
    }


class Captain(User):
    __tablename__ = 'captain'
    id = db.Column(None, db.ForeignKey('user.id'), primary_key=True)
    tournament = db.Column(db.Integer, db.ForeignKey('tournament.id'))

    __mapper_args__ = {
        'polymorphic_identity': 'captain'
    }


class Tournament(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    organizer_id = db.Column(db.Integer, db.ForeignKey('organizer.id'))
    organizer = db.relationship('Organizer', foreign_keys=[organizer_id])

    judge_id = db.Column(db.Integer, db.ForeignKey('judge.id'))
    judge = db.relationship('Judge', foreign_keys=[judge_id])

    captains = db.relationship('Captain', lazy='dynamic')
