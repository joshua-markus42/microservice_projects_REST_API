from . import db
import enum


class StatusType(enum.Enum):
    doing_nothing = 'nothing'
    calculating = 'calculating'
    complete = 'complete'


class Projects(db.Model):
    __tablename__ = 'Projects'
    id = db.Column(db.Integer, db.ForeignKey('projects.id'), primary_key=True)
    contract_id = db.Column(db.Integer)
    user_id = db.Column(db.Integer)
    # status = db.Column(db.ChoiceType(StatusType))

class Data(db.Model):
    __tablename__ = 'Data'
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.relationship('Projects')
