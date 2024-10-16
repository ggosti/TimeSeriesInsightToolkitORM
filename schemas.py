from marshmallow import Schema, fields
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, auto_field
from models import Base, RawEvent, RawRecord, RawGroup, Event, Group, Record, create_engine #, Step, Aggregate

#from sqlalchemy import Column, Integer, String, ForeignKey, Table,create_engine #Column, Integer, String, ForeignKey, Table, create_engine
from sqlalchemy.orm import sessionmaker, declarative_base #, relationship

class RawRecordSchema(SQLAlchemyAutoSchema):
    """
    Schema for Raw Record model.
    
    >>> engine = create_engine('sqlite:///:memory:')
    >>> Base.metadata.create_all(engine)
    >>> Session = sessionmaker(bind=engine)
    >>> session = Session()
        
    Example JSON data
    >>> json_raw_record = {'name': 'Test Raw Record 1', 'rawgroup_id':1}

    Deserialize JSON data into a User object
    >>> raw_record_schema = RawRecordSchema()
    >>> raw_record = raw_record_schema.load(json_raw_record, session=session)
    >>> raw_record.name
    'Test Raw Record 1'
    
    Add to the session and commit to the database
    >>> session.add(raw_record)
    >>> session.commit()
    
    >>> [r.name for r in session.query(RawRecord).all()]
    ['Test Raw Record 1']

    >>> [r.id for r in session.query(RawRecord).all()]
    [1]
    
    >>> raw_record_schema.dump(session.query(RawRecord).first())['id']
    1
    >>> raw_record_schema.dump(session.query(RawRecord).first())['name']
    'Test Raw Record 1'
    >>> raw_record_schema.dump(session.query(RawRecord).first())['rawgroup_id']
    1
    """
    class Meta:
        model = RawRecord
        load_instance = True # Automatically create instances of the Record model
        include_fk = True  # Include foreign keys (e.g., group_id)

    ## Many-to-many relationship: Aggregates that contain this record
    #aggregates = fields.Nested('AggregateSchema', many=True, exclude=('records',))

class RawGroupSchema(SQLAlchemyAutoSchema):
    """
    Schema for Raw Group model.
    
    >>> engine = create_engine('sqlite:///:memory:')
    >>> Base.metadata.create_all(engine)
    >>> Session = sessionmaker(bind=engine)
    >>> session = Session()
        
    Example JSON data
    >>> json_raw_group = {'name': 'Test Raw Group', 'rawevent_id':1}

    Deserialize JSON data into a User object
    >>> raw_group_schema = RawGroupSchema()
    >>> raw_group = raw_group_schema.load(json_raw_group, session=session)
    >>> raw_group.name
    'Test Raw Group'
    
    Add to the session and commit to the database
    >>> session.add(raw_group)
    >>> session.commit()
    
    >>> [g.name for g in session.query(RawGroup).all()]
    ['Test Raw Group']

    >>> [g.id for g in session.query(RawGroup).all()]
    [1]
    
    >>> raw_group_schema.dump(session.query(RawGroup).first())['id']
    1
    >>> raw_group_schema.dump(session.query(RawGroup).first())['name']
    'Test Raw Group'
    >>> raw_group_schema.dump(session.query(RawGroup).first())['rawevent_id']
    1
    """
    class Meta:
        model = RawGroup
        load_instance = True
        include_fk = True  # Include foreign keys (e.g., event_id)
        
    ## Nested relationship: Aggregates in the group
    #aggregates = fields.Nested(AggregateSchema, many=True)

    ## Nested relationship: Records in the group
    #records = fields.Nested(RecordSchema, many=True)

class RawEventSchema(SQLAlchemyAutoSchema):
    """
    Schema for Raw Event model.
    
    >>> engine = create_engine('sqlite:///:memory:')
    >>> Base.metadata.create_all(engine)
    >>> Session = sessionmaker(bind=engine)
    >>> session = Session()
        
    Example JSON data
    >>> json_raw_event = {'name': 'Test Raw Event', }

    Deserialize JSON data into a User object
    >>> raw_event_schema = RawEventSchema()
    >>> raw_event = raw_event_schema.load(json_raw_event, session=session)
    >>> raw_event.name
    'Test Raw Event'
    
    Add to the session and commit to the database
    >>> session.add(raw_event)
    >>> session.commit()
    
    >>> [g.name for g in session.query(RawEvent).all()]
    ['Test Raw Event']

    >>> [g.id for g in session.query(RawEvent).all()]
    [1]
    
    >>> raw_event_schema.dump(session.query(RawEvent).first())['id']
    1
    >>> raw_event_schema.dump(session.query(RawEvent).first())['name']
    'Test Raw Event'
    """
    
    class Meta:
        model = RawEvent
        load_instance = True
        include_fk = True  # Include foreign keys (e.g., step_id)

    # Fields to make optional during deserialization
    #startDate = fields.Date(required=False)  # Optional field
    #endDate = fields.Date(required=False)  # Optional field
    #location = fields.String(required=False)  # Optional field
    #notes = fields.String(required=False)  # Optional field
    #path = fields.String(required=False)  # Optional field   
    
    #rawgroups = fields.List(fields.Nested(RawGroupSchema))


# # Schema for the Aggregate model
# class AggregateSchema(SQLAlchemyAutoSchema):
#     """
#     Schema for Aggregate model.
    
#     >>> engine = create_engine('sqlite:///:memory:')
#     >>> Base.metadata.create_all(engine)
#     >>> Session = sessionmaker(bind=engine)
#     >>> session = Session()
        
#     Example JSON data
#     >>> json_aggregate = {'name': 'Test Aggregate 1', 'group_id':1}

#     Deserialize JSON data into a User object
#     >>> aggregate_schema = AggregateSchema()
#     >>> aggregate = aggregate_schema.load(json_aggregate, session=session)
#     >>> aggregate.name
#     'Test Aggregate 1'
    
#     Add to the session and commit to the database
#     >>> session.add(aggregate)
#     >>> session.commit()
    
#     >>> [r.name for r in session.query(Aggregate).all()]
#     ['Test Aggregate 1']

#     >>> [r.id for r in session.query(Aggregate).all()]
#     [1]
    
#     >>> aggregate_schema.dump(session.query(Aggregate).first())['id']
#     1
#     >>> aggregate_schema.dump(session.query(Aggregate).first())['name']
#     'Test Aggregate 1'
#     >>> aggregate_schema.dump(session.query(Aggregate).first())['group_id']
#     1
#     >>> len(aggregate_schema.dump(session.query(Aggregate).first())['records'])
#     0
#     """
#     class Meta:
#         model = Aggregate
#         load_instance = True  # Automatically create instances of the Aggregate model
#         include_fk = True  # Include foreign keys (e.g., group_id)

#     # Many-to-many relationship: Subset of records
#     records = fields.Nested(RecordSchema, many=True)


class EventSchema(SQLAlchemyAutoSchema):
    """
    Schema for Event model.
    
    >>> engine = create_engine('sqlite:///:memory:')
    >>> Base.metadata.create_all(engine)
    >>> Session = sessionmaker(bind=engine)
    >>> session = Session()
        
    Example JSON data
    >>> json_event = {'name': 'Test Event', 'step_id':1}

    Deserialize JSON data into a User object
    >>> event_schema = EventSchema()
    >>> event = event_schema.load(json_event, session=session)
    >>> event.name
    'Test Event'
    
    Add to the session and commit to the database
    >>> session.add(event)
    >>> session.commit()
    
    >>> [g.name for g in session.query(Event).all()]
    ['Test Event']

    >>> [g.id for g in session.query(Event).all()]
    [1]
    
    >>> event_schema.dump(session.query(Event).first())['id']
    1
    >>> event_schema.dump(session.query(Event).first())['name']
    'Test Event'
    >>> event_schema.dump(session.query(Event).first())['step_id']
    1
    """
    
    class Meta:
        model = Event
        load_instance = True
        include_fk = True  # Include foreign keys (e.g., step_id)
        

    # Nested relationship: Records in the group
    rawevent = fields.Nested(RawEventSchema, only=('id', 'name'))
    #groups = fields.List(fields.Nested(GroupSchema))

class GroupSchema(SQLAlchemyAutoSchema):
    """
    Schema for Group model.
    
    >>> engine = create_engine('sqlite:///:memory:')
    >>> Base.metadata.create_all(engine)
    >>> Session = sessionmaker(bind=engine)
    >>> session = Session()
        
    Example JSON data
    >>> json_group = {'name': 'Test Group', 'event_id':1}

    Deserialize JSON data into a User object
    >>> group_schema = GroupSchema()
    >>> group = group_schema.load(json_group, session=session)
    >>> group.name
    'Test Group'
    
    Add to the session and commit to the database
    >>> session.add(group)
    >>> session.commit()
    
    >>> [g.name for g in session.query(Group).all()]
    ['Test Group']

    >>> [g.id for g in session.query(Group).all()]
    [1]
    
    >>> group_schema.dump(session.query(Group).first())['id']
    1
    >>> group_schema.dump(session.query(Group).first())['name']
    'Test Group'
    >>> group_schema.dump(session.query(Group).first())['event_id']
    1
    """
    class Meta:
        model = Group
        load_instance = True
        include_fk = True  # Include foreign keys (e.g., event_id)
        
    ## Nested relationship: Aggregates in the group
    rawgroup = fields.Nested(RawGroupSchema, only=('id', 'name'))
    event = fields.Nested(EventSchema, only=('id', 'name'))
    #aggregates = fields.Nested(AggregateSchema, many=True)
    #records = fields.Nested(RecordSchema, many=True)


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

    ## Nested relationship: Aggregates in the group
    rawrecord = fields.Nested(RawRecordSchema, only=('id', 'name'))
    group = fields.Nested(GroupSchema, only=('id', 'name'))
    ## Many-to-many relationship: Aggregates that contain this record
    #aggregates = fields.Nested('AggregateSchema', many=True, exclude=('records',))

# class StepSchema(SQLAlchemyAutoSchema):
#     """
#     Schema for Step model.
    
#     >>> engine = create_engine('sqlite:///:memory:')
#     >>> Base.metadata.create_all(engine)
#     >>> Session = sessionmaker(bind=engine)
#     >>> session = Session()
        
#     Example JSON data
#     >>> json_step = {'name': 'Test Step'}

#     Deserialize JSON data into a User object
#     >>> step_schema = StepSchema()
#     >>> step = step_schema.load(json_step, session=session)
#     >>> step.name
#     'Test Step'
    
#     Add to the session and commit to the database
#     >>> session.add(step)
#     >>> session.commit()
    
#     >>> [g.name for g in session.query(Step).all()]
#     ['Test Step']

#     >>> [g.id for g in session.query(Step).all()]
#     [1]
    
#     >>> step_schema.dump(session.query(Step).first())['id']
#     1
#     >>> step_schema.dump(session.query(Step).first())['name']
#     'Test Step'
#     """
    
#     class Meta:
#         model = Step
#         load_instance = True
#     #events = fields.List(fields.Nested(EventSchema))
