from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import text

from . import db


class Projects(db.Model):
    id = db.Column(UUID(as_uuid=True), primary_key=True, server_default=text("uuid_generate_v4()"))
    status = db.Column(db.String())
    rooms_data = db.relationship('RoomsData')


class RoomsData(db.Model):
    id = db.Column(UUID(as_uuid=True), primary_key=True, server_default=text("uuid_generate_v4()"))
    project_id = db.Column(UUID(as_uuid=True), db.ForeignKey('projects.id'))
    address = db.Column(db.String(80))
    city = db.Column(db.String(80))
    square = db.Column(db.Integer())
    living_square = db.Column(db.Integer())
    price = db.Column(db.Integer())
    published_date = db.Column(db.DateTime())
    rooms = db.Column(db.Integer())
    toilets = db.Column(db.Integer())


