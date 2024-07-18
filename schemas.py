from marshmallow import Schema, fields
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, auto_field
from models import Step, Event, Group, Record

class RecordSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Record
        load_instance = True

class GroupSchema(SQLAlchemyAutoSchema):
    records = fields.List(fields.Nested(RecordSchema))
    
    class Meta:
        model = Group
        load_instance = True

class EventSchema(SQLAlchemyAutoSchema):
    groups = fields.List(fields.Nested(GroupSchema))
    
    class Meta:
        model = Event
        load_instance = True

class StepSchema(SQLAlchemyAutoSchema):
    events = fields.List(fields.Nested(EventSchema))
    
    class Meta:
        model = Step
        load_instance = True