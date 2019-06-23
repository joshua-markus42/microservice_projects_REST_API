from sqlalchemy import text
from sqlalchemy.dialects.postgresql import UUID
from . import db, ma


class Projects(db.Model):
    id = db.Column(UUID(as_uuid=True), primary_key=True, server_default=text("uuid_generate_v4()"))
    name = db.Column(db.String())
    status = db.Column(db.String())
    room_data = db.relationship('Data', backref="project")

    def __init__(self, name, status):
        self.name = name
        self.status = status


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


# Project Schema
class ProjectsSchema(ma.Schema):
    class Meta:
        # model = Projects
        fields = ('id', 'name', 'status')


# Init schema
project_schema = ProjectsSchema(strict=True)
projects_schema = ProjectsSchema(many=True, strict=True)


# Data Schema
class DataSchema(ma.Schema):
    class Meta:
        # model = Data
        fields = ('id', 'project_id', 'address', 'city', 'square', 'living_square', 'currency_value', 'currency',
                  'published_date', 'rooms', 'toilets')

    projects = ma.Nested(ProjectsSchema)


# Init data schema
data_schema = DataSchema(strict=True)
datas_schema = DataSchema(many=True, strict=True)

