from uuid import uuid4
from sqlalchemy.dialects.postgresql import UUID

from . import db


class Projects(db.Model):
    id = db.Column(UUID(as_uuid=True), default=uuid4(), primary_key=True, uniqe=True)
    contract_id = id.Column(UUID(as_uuid=True))
    user_id = db.Column(UUID(as_uuid=True))
    status = db.String()
    rooms_data = db.relationship('RoomsData')


class RoomsData(db.Model):
    id = db.Column(UUID(as_uuid=True), default=uuid4(), primary_key=True, uniqe=True)
    project_id = db.Column(UUID(as_uuid=True), db.ForeignKey('projects.id'))
