from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import text

from . import db


class Projects(db.Model):
    id = db.Column(UUID(as_uuid=True), primary_key=True, server_default=text("uuid_generate_v4()"))
    name = db.Column(db.String())
    status = db.Column(db.String())
    rooms_data = db.relationship('Data')


class Data(db.Model):
    id = db.Column(UUID(as_uuid=True), primary_key=True, server_default=text("uuid_generate_v4()"))
    project_id = db.Column(UUID(as_uuid=True), db.ForeignKey('projects.id'))
    address = db.Column(db.String(80))
    city = db.Column(db.String(80))
    square = db.Column(db.Float())
    living_square = db.Column(db.Float())
    currency_value = db.Column(db.Float())
    currency = db.Column(db.String)
    published_date = db.Column(db.DateTime())
    rooms = db.Column(db.Integer())
    toilets = db.Column(db.Integer())

    def __init__(self, project_id, address, city, square, living_square,
                 currency_value, currency, published_date, rooms, toilets):
        self.project_id = project_id
        self.address = address
        self.city = city
        self.square = square
        self.living_square = living_square
        self.currency_value = currency_value
        self.currency = currency
        self.published_date = published_date
        self.rooms = rooms
        self.toilets = toilets