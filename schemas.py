from marshmallow import Schema, fields
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, auto_field
from models import Step, Event, Group, Record, Aggregate

class RecordSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Record
        load_instance = True # Automatically create instances of the Record model
        include_fk = True  # Include foreign keys (e.g., group_id)

    # Many-to-many relationship: Aggregates that contain this record
    aggregates = fields.Nested('AggregateSchema', many=True, exclude=('records',))


# Schema for the Aggregate model
class AggregateSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Aggregate
        load_instance = True  # Automatically create instances of the Aggregate model
        include_fk = True  # Include foreign keys (e.g., group_id)

    # Many-to-many relationship: Subset of records
    records = fields.Nested(RecordSchema, many=True)

class GroupSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Group
        load_instance = True
        
    # Nested relationship: Aggregates in the group
    aggregates = fields.Nested(AggregateSchema, many=True)

    # Nested relationship: Records in the group
    records = fields.Nested(RecordSchema, many=True)

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