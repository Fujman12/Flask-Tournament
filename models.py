from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from enums import positions
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


judge_tournaments = db.Table('judge_tournaments',
     db.Column('judge_id', db.Integer, db.ForeignKey('judge.id')),
     db.Column('tournament_id', db.Integer, db.ForeignKey('tournament.id')),
)


class Judge(User):
    __tablename__ = 'judge'
    id = db.Column(None, db.ForeignKey('user.id'), primary_key=True)
    tournaments = db.relationship('Tournament', secondary=judge_tournaments,
                                  backref=db.backref('judges', lazy='dynamic'))

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
    number_of_teams = db.Column(db.Integer)
    captains = db.relationship('Captain', lazy='dynamic')
    current_round = db.Column(db.Integer, default=1)

    def next_round(self):
        all_assessed = True
        current_pairs = []

        for pair in self.pairs:
            if pair.round == self.current_round:
                current_pairs.append(pair)

        for pair in current_pairs:
            if not pair.assessed:
                all_assessed = False

        winners = []

        if all_assessed:

            for pair in current_pairs:
                if pair.captains[0].team.total_score > pair.captains[1].team.total_score:
                    winners.append(pair.captains[0])
                else:
                    winners.append(pair.captains[1])

                db.session.add(pair)
                db.session.commit()
            print(winners)

            for cap in self.captains:
                cap.team.total_score = 0
                for member in cap.team.members:
                    member.score = 0
                    member.assessed = False
                    db.session.add(member)
                    db.session.commit()
                db.session.add(cap)
                db.session.commit()

            self.current_round += 1
            p = Pair(tournament=self)
            p.round = self.current_round
            for winner in winners:
                if len(p.captains) < 2:
                    p.captains.append(winner)
                else:
                    p = Pair(tournament=self)
                    p.round = self.current_round
                    p.captains.append(winner)
                db.session.add(p)
                db.session.add(self)
                db.session.commit()

            return True

        return False

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
        }

    def __repr__(self):
        return "Tournament {} (id-{}): Organizer - {}".format(self.name, self.id, self.organizer.username)


class Team(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=True)
    total_score = db.Column(db.DECIMAL(4, 2))

    captain_id = db.Column(db.Integer, db.ForeignKey('captain.id'))

    def count_score(self):
        total_score = 0
        for member in self.members:
            if member.score:
                total_score += member.score

        self.total_score = total_score

        db.session.add(self)
        db.session.commit()

        return None

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name
        }

    def __repr__(self):
        return "Team({}) {}: Captain - {}".format(self.id, self.name, self.captain.username)


class Member(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30))
    email = db.Column(db.String(50), unique=True)
    role = db.Column(db.String(20))
    score = db.Column(db.DECIMAL(4, 2))

    team_id = db.Column(db.Integer, db.ForeignKey('team.id'))
    team = db.relationship('Team', foreign_keys=[team_id], backref='members')

    assessed = db.Column(db.Boolean, default=False)

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name
        }

    def __repr__(self):
        return "{} from team {}".format(self.name, self.team.name)


captain_pair = db.Table('captain_pair',
     db.Column('captain_id', db.Integer, db.ForeignKey('captain.id')),
     db.Column('pair_id', db.Integer, db.ForeignKey('pair.id')),
)


class Pair(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    round = db.Column(db.Integer, default=1)
    captains = db.relationship('Captain', secondary=captain_pair,
                               backref=db.backref('pairs', lazy='dynamic'))
    tournament_id = db.Column(db.Integer, db.ForeignKey('tournament.id'))
    tournament = db.relationship('Tournament', foreign_keys=[tournament_id], backref='pairs')

    cap0_score = db.Column(db.DECIMAL(4, 2))
    cap1_score = db.Column(db.DECIMAL(4, 2))

    assessed = db.Column(db.Boolean, default=False)

    def is_assessed(self):
        bool_assessed = True
        common_positions = self.common_positions()
        for pos in common_positions:
            for member in self.captains[0].team.members:
                if member.role == pos:
                    if not member.assessed:
                        bool_assessed = False
            for member in self.captains[1].team.members:
                if member.role == pos:
                    if not member.assessed:
                        bool_assessed = False
        print('bool assessed {}'.format(bool_assessed))
        self.assessed = bool_assessed
        print('self assessed {}'.format(self.assessed))
        db.session.add(self)
        db.session.commit()
        if bool_assessed:
            self.update_scores()
            self.tournament.next_round()

        return bool_assessed

    def common_positions(self):
        common_positions =[]
        for pos in positions:
            member0 = None
            member0 = None
            for member in self.captains[0].team.members:
                if member.role == pos:
                    member0 = member
            for member in self.captains[1].team.members:
                if member.role == pos:
                    member1 = member

            if member0 is not None and member1 is not None:
                common_positions.append(pos)

        return common_positions

    def update_scores(self):
        print('hi update score')
        self.cap0_score = self.captains[0].team.total_score
        self.cap1_score = self.captains[1].team.total_score

        db.session.add(self)
        db.session.commit()

        return True

    def serialize(self):
        return {
            'id': self.id,
            'round': self.round,
            'team0': self.captains[0].team.serialize(),
            'team1': self.captains[1].team.serialize()
        }

    def __repr__(self):
        return "Pair #{} '{}' vs '{}'. Round #{}".format(self.id,
                                                         self.captains[0].team.name,
                                                         self.captains[1].team.name,
                                                         self.round)
