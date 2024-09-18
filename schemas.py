from marshmallow import Schema, fields
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, auto_field
from models import Step, Event, Group, Record, Aggregate, Base, create_engine

#from sqlalchemy import Column, Integer, String, ForeignKey, Table,create_engine #Column, Integer, String, ForeignKey, Table, create_engine
from sqlalchemy.orm import sessionmaker, declarative_base #, relationship


class RecordSchema(SQLAlchemyAutoSchema):
    """
    Schema for Record model.
    
    >>> engine = create_engine('sqlite:///:memory:')
    >>> Base.metadata.create_all(engine)
    >>> Session = sessionmaker(bind=engine)
    >>> session = Session()
        
    Example JSON data
    >>> json_record = {'name': 'Test Record 1','version': 'testVer', 'group_id':1}

    Deserialize JSON data into a User object
    >>> record_schema = RecordSchema()
    >>> record = record_schema.load(json_record, session=session)
    >>> record.name
    'Test Record 1'
    
    Add to the session and commit to the database
    >>> session.add(record)
    >>> session.commit()
    
    >>> [r.name for r in session.query(Record).all()]
    ['Test Record 1']

    >>> [r.id for r in session.query(Record).all()]
    [1]
    
    >>> record_schema.dump(session.query(Record).first())['id']
    1
    >>> record_schema.dump(session.query(Record).first())['name']
    'Test Record 1'
    >>> record_schema.dump(session.query(Record).first())['version']
    'testVer'
    >>> record_schema.dump(session.query(Record).first())['group_id']
    1
    """
    class Meta:
        model = Record
        load_instance = True # Automatically create instances of the Record model
        include_fk = True  # Include foreign keys (e.g., group_id)

    ## Many-to-many relationship: Aggregates that contain this record
    #aggregates = fields.Nested('AggregateSchema', many=True, exclude=('records',))


# Schema for the Aggregate model
class AggregateSchema(SQLAlchemyAutoSchema):
    """
    Aggregate for Record model.
    
    >>> engine = create_engine('sqlite:///:memory:')
    >>> Base.metadata.create_all(engine)
    >>> Session = sessionmaker(bind=engine)
    >>> session = Session()
        
    Example JSON data
    >>> json_aggregate = {'name': 'Test Aggregate 1', 'group_id':1}

    Deserialize JSON data into a User object
    >>> aggregate_schema = AggregateSchema()
    >>> aggregate = aggregate_schema.load(json_aggregate, session=session)
    >>> aggregate.name
    'Test Aggregate 1'
    
    Add to the session and commit to the database
    >>> session.add(aggregate)
    >>> session.commit()
    
    >>> [r.name for r in session.query(Aggregate).all()]
    ['Test Aggregate 1']

    >>> [r.id for r in session.query(Aggregate).all()]
    [1]
    
    >>> aggregate_schema.dump(session.query(Aggregate).first())['id']
    1
    >>> aggregate_schema.dump(session.query(Aggregate).first())['name']
    'Test Aggregate 1'
    >>> aggregate_schema.dump(session.query(Aggregate).first())['group_id']
    1
    >>> len(aggregate_schema.dump(session.query(Aggregate).first())['records'])
    0
    """
    class Meta:
        model = Aggregate
        load_instance = True  # Automatically create instances of the Aggregate model
        include_fk = True  # Include foreign keys (e.g., group_id)

    # Many-to-many relationship: Subset of records
    records = fields.Nested(RecordSchema, many=True)

class GroupSchema(SQLAlchemyAutoSchema):
    """
    Schema for Record model.
    
    >>> engine = create_engine('sqlite:///:memory:')
    >>> Base.metadata.create_all(engine)
    >>> Session = sessionmaker(bind=engine)
    >>> session = Session()
        
    Example JSON data
    >>> json_record = {'name': 'Test Record 1','version': 'testVer', 'group_id':1}

    Deserialize JSON data into a User object
    >>> record_schema = RecordSchema()
    >>> record = record_schema.load(json_record, session=session)
    >>> record.name
    'Test Record 1'
    
    Add to the session and commit to the database
    >>> session.add(record)
    >>> session.commit()
    
    >>> [r.name for r in session.query(Record).all()]
    ['Test Record 1']

    >>> [r.id for r in session.query(Record).all()]
    [1]
    
    >>> record_schema.dump(session.query(Record).first())['id']
    1
    >>> record_schema.dump(session.query(Record).first())['name']
    'Test Record 1'
    >>> record_schema.dump(session.query(Record).first())['version']
    'testVer'
    >>> record_schema.dump(session.query(Record).first())['group_id']
    1
    """
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
