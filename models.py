from sqlalchemy import Column, Integer, Numeric, String, Date, DateTime, ForeignKey, Table, create_engine
from sqlalchemy.orm import relationship, sessionmaker, declarative_base

Base = declarative_base()

# Association table for Aggregate <-> Record
aggregate_records = Table(
    'aggregate_records', Base.metadata,
    Column('aggregate_id', Integer, ForeignKey('aggregates.id')),
    Column('record_id', Integer, ForeignKey('records.id'))
)

# Association table for Event <-> Step
event_steps = Table(
    'event_step', Base.metadata,
    Column('step_id', Integer, ForeignKey('steps.id')),
    Column('event_id', Integer, ForeignKey('events.id'))
)


class RawEvent(Base):
    """
    Raw event model for managing events with groups of records from acquired raw folser.

    >>> engine = create_engine('sqlite:///:memory:')
    >>> Base.metadata.create_all(engine)
    >>> Session = sessionmaker(bind=engine)
    >>> session = Session()

    >>> event1 = RawEvent(id=1, name="Test Raw Event 1")
    >>> session.add(event1)
    >>> event2 = RawEvent(id=2, name="Test Raw Event 2")
    >>> session.add(event2)
    >>> session.commit()

    >>> event1.name
    'Test Raw Event 1'

    >>> event2.name
    'Test Raw Event 2'

    >>> session.query(Event).first().name
    'Test Raw Event 1'
    
    >>> session.query(Event).first().event_name
    1
    """
    __tablename__ = 'rawEvent'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    startDate = Column(Date, nullable=True)
    endDate = Column(Date, nullable=True)
    event_name = Column(String, nullable=True)
    notes = Column(String, nullable=True)
    groups = relationship('Group', back_populates='event')


# class rawGroup(Base):
#     """
#     Raw group model for managing groups of records from acquired raw folser.

#     >>> engine = create_engine('sqlite:///:memory:')
#     >>> Base.metadata.create_all(engine)
#     >>> Session = sessionmaker(bind=engine)
#     >>> session = Session()

#     >>> group1 = rawGroup(id=1, name="Test Raw Group 1", event_name="Event 1")
#     >>> session.add(group1)
#     >>> group2 = rawGroup(id=2, name="Test Raw Group 2", event_name="Event 2")
#     >>> session.add(group2)
#     >>> session.commit()

#     >>> group1.name
#     'Test Raw Group 1'

#     >>> group2.name
#     'Test Raw Group 2'

#     >>> session.query(Group).first().name
#     'Test Raw Group 1'
    
#     >>> session.query(Group).first().event_name
#     1
#     """
#     __tablename__ = 'rawGroup'
#     id = Column(Integer, primary_key=True)
#     name = Column(String, nullable=False)
#     startDate = Column(Date, nullable=True)
#     endDate = Column(Date, nullable=True)
#     event_name = Column(String, nullable=True)
#     notes = Column(String, nullable=True)

# class rawRecord(Base):
#     __tablename__ = 'rawRecord'
#     id = Column(Integer, primary_key=True)
#     name = Column(String, nullable=False)
#     startTime = Column(DateTime, nullable=True)
#     endTime = Column(DateTime, nullable=True)
#     totalTime = Column(Numeric, nullable=True)
#     totalVariation = Column(Numeric, nullable=True)
#     navigation = Column(String, nullable=True)
#     event_name = Column(String, nullable=True)
#     notes = Column(String, nullable=True)

# class Step(Base):
#     """
#     Steps model for managing groups of records and aggregates from events.

#     >>> engine = create_engine('sqlite:///:memory:')
#     >>> Base.metadata.create_all(engine)
#     >>> Session = sessionmaker(bind=engine)
#     >>> session = Session()

#     >>> step1 = Step(id=1, name="Test Step 1")
#     >>> session.add(step1)
#     >>> step2 = Step(id=2, name="Test Step 2")
#     >>> session.add(step2)
#     >>> session.commit()

#     >>> step1.name
#     'Test Step 1'

#     >>> session.query(Step).first().name
#     'Test Step 1'

#     >>> [s.name for s in session.query(Step).all()]
#     ['Test Step 1', 'Test Step 2']
    
#     """
#     __tablename__ = 'steps'
#     id = Column(Integer, primary_key=True)
#     name = Column(String, nullable=False)
#     eventsInStep = relationship('EventFolder', back_populates='step')
#     #events = relationship('Event', back_populates='steps')
#     events = relationship('Event', secondary=event_steps, back_populates='steps')

# class EventFolder(Base):
#     """
#     EventsFolder model for managing groups of records and aggregates from events folfers.
#     Each step may have an event folder, \
#     but a single event may corrispond to different events foders in different steps.

#     >>> engine = create_engine('sqlite:///:memory:')
#     >>> Base.metadata.create_all(engine)
#     >>> Session = sessionmaker(bind=engine)
#     >>> session = Session()

#     >>> step1 = Step(id=1, name="Test Step 1")
#     >>> session.add(step1)
#     >>> step2 = Step(id=2, name="Test Step 2")
#     >>> session.add(step2)
#     >>> session.commit()

#     >>> eventFolder1 = EventFolder(id=1, name="Test Event 1", step_id=step1.id)
#     >>> session.add(eventFolder1)
#     >>> eventFolder2 = EventFolder(id=2, name="Test Event 2", step_id=step1.id)
#     >>> session.add(eventFolder2)
#     >>> eventFolder3 = EventFolder(id=3, name="Test Event 1", step_id=step2.id)
#     >>> session.add(eventFolder3)
#     >>> session.commit()

#     >>> eventFolder1.name
#     'Test Event 1'

#     >>> eventFolder2.name
#     'Test Event 2'

#     >>> session.query(EventFolder).first().name
#     'Test Event 1'
    
#     >>> session.query(EventFolder).first().step_id
#     1

#     >>> [(ef.id,ef.name,ef.step_id) for ef in session.query(EventFolder).all()]
#     [(1, 'Test Event 1', 1), (2, 'Test Event 2', 1), (3, 'Test Event 1', 2)]

#     >>> [(type(ef).__name__) for ef in session.query(EventFolder).all()]
#     ['EventFolder', 'EventFolder', 'EventFolder']

#     >>> [(type(ef.step).__name__) for ef in session.query(EventFolder).all()]
#     ['Step', 'Step', 'Step']

#     """
#     __tablename__ = 'eventFolders'
#     id = Column(Integer, primary_key=True)
#     name = Column(String, nullable=False)
#     step_id = Column(Integer, ForeignKey('steps.id'), nullable=False)
#     step = relationship('Step', back_populates='eventsInStep')

# class Event(Base):
#     """
#     Events model for managing groups of records and aggregates from events.

#     >>> engine = create_engine('sqlite:///:memory:')
#     >>> Base.metadata.create_all(engine)
#     >>> Session = sessionmaker(bind=engine)
#     >>> session = Session()

#     >>> step1 = Step(id=1, name="Test Step 1")
#     >>> session.add(step1)
#     >>> step2 = Step(id=2, name="Test Step 2")
#     >>> session.add(step2)
#     >>> session.commit()

#     >>> eventFolder1 = EventFolder(id=1, name="Test Event 1", step_id=step1.id)
#     >>> session.add(eventFolder1)
#     >>> eventFolder2 = EventFolder(id=2, name="Test Event 2", step_id=step1.id)
#     >>> session.add(eventFolder2)
#     >>> eventFolder3 = EventFolder(id=3, name="Test Event 1", step_id=step2.id)
#     >>> session.add(eventFolder3)
#     >>> session.commit()

#     >>> [(ef.id,ef.name,ef.step_id) for ef in session.query(EventFolder).all()]

#     TODO:
#     >>> event1 = Event(id=1, name="Test Event 1", step_id=step.id)
#     >>> session.add(event1)
#     >>> event2 = Event(id=2, name="Test Event 2", step_id=step.id)
#     >>> session.add(event2)
#     >>> session.commit()

#     >>> event1.name
#     'Test Event 1'

#     >>> event2.name
#     'Test Event 2'

#     >>> session.query(Event).first().name
#     'Test Event 1'
    
#     >>> session.query(Event).first().step_id
#     1
#     """
#     __tablename__ = 'events'
#     id = Column(Integer, primary_key=True)
#     name = Column(String, nullable=False)
#     #steps_id = Column(Integer, ForeignKey('steps.id'), nullable=False)
#     #step = relationship('Step', back_populates='events')
#     # Many-to-many relationship with Record
#     steps = relationship('Step', secondary=event_steps, back_populates='events')
#     groups = relationship('Group', back_populates='event')

# class Group(Base):
#     """
#     Group model for managing groups of records and aggregates from events.

#     >>> engine = create_engine('sqlite:///:memory:')
#     >>> Base.metadata.create_all(engine)
#     >>> Session = sessionmaker(bind=engine)
#     >>> session = Session()

#     >>> step = Step(id=1, name="Test Step")
#     >>> session.add(step)
#     >>> session.commit()

#     >>> event = Event(id=1, name="Test Event", step_id=step.id)
#     >>> session.add(event)
#     >>> session.commit()

#     >>> group1 = Group(id=1, name="Test Group 1", event_id=event.id)
#     >>> session.add(group1)
#     >>> group2 = Group(id=2, name="Test Group 2", event_id=event.id)
#     >>> session.add(group2)
#     >>> session.commit()

#     >>> event.name
#     'Test Event'

#     >>> group1.name
#     'Test Group 1'

#     >>> group2.name
#     'Test Group 2'

#     >>> session.query(Group).first().name
#     'Test Group 1'
    
#     >>> session.query(Group).first().event_id
#     1
#     """
#     __tablename__ = 'groups'
#     id = Column(Integer, primary_key=True)
#     name = Column(String, nullable=False)
#     event_id = Column(Integer, ForeignKey('events.id'), nullable=False)
#     event = relationship('Event', back_populates='groups')
#     records = relationship('Record', back_populates='group')
#     aggregates = relationship('Aggregate', back_populates='group')

# class Record(Base):
#     """
#     Group model for managing groups of records and aggregates from events.

#     >>> engine = create_engine('sqlite:///:memory:')
#     >>> Base.metadata.create_all(engine)
#     >>> Session = sessionmaker(bind=engine)
#     >>> session = Session()

#     >>> step = Step(id=1, name="Test Step")
#     >>> session.add(step)
#     >>> session.commit()

#     >>> event = Event(id=1, name="Test Event", step_id=step.id)
#     >>> session.add(event)
#     >>> session.commit()

#     >>> group = Group(id=1, name="Test Group", event_id=event.id)
#     >>> session.add(group)
#     >>> session.commit()
    
#     >>> record = Record(id=1, name="Test Record", group_id=group.id)
#     >>> session.add(record)
#     >>> session.commit()

#     >>> event.name
#     'Test Event'

#     >>> group.name
#     'Test Group'

#     >>> session.query(Group).first().name
#     'Test Group'
    
#     >>> session.query(Record).first().name
#     'Test Record'
#     >>> session.query(Record).first().id
#     1
    
#     >>> session.query(Record).first().group_id
#     1
    
    
#     """
#     __tablename__ = 'records'
#     id = Column(Integer, primary_key=True)
#     name = Column(String, nullable=False)
#     version = Column(String, nullable=True)
#     group_id = Column(Integer, ForeignKey('groups.id'), nullable=False)
    
#     # Relationship to Group and Aggregate
#     group = relationship('Group', back_populates='records')
#     aggregates = relationship('Aggregate', secondary=aggregate_records, back_populates='records')


# class Aggregate(Base):
#     """
#     Aggregate model for managing aggregates of records from groups and events.

#     >>> engine = create_engine('sqlite:///:memory:')
#     >>> Base.metadata.create_all(engine)
#     >>> Session = sessionmaker(bind=engine)
#     >>> session = Session()
    
#     >>> step = Step(id=1, name="Test Step")
#     >>> session.add(step)
#     >>> session.commit()

#     >>> event = Event(id=1, name="Test Event", step_id=step.id)
#     >>> session.add(event)
#     >>> session.commit()

#     >>> group = Group(id=1, name="Test Group", event_id=event.id)
#     >>> session.add(group)
#     >>> session.commit()

#     >>> record1 = Record(id=1, name="Record 1", group_id=group.id)
#     >>> record2 = Record(id=2, name="Record 2", group_id=group.id)
#     >>> record3 = Record(id=3, name="Record 3", group_id=group.id)
#     >>> session.add_all([record1, record2, record3])
#     >>> session.commit()

#     >>> aggregate = Aggregate(id=1,name="Test Aggregate", group_id=group.id, records=[record1, record3])
#     >>> session.add(aggregate)
#     >>> session.commit()

#     >>> [r.id for r in session.query(Aggregate).first().records]
#     [1, 3]

#     >>> len(session.query(Aggregate).first().records)
#     2
#     """
    
#     __tablename__ = 'aggregates'
#     id = Column(Integer, primary_key=True)
#     name = Column(String, nullable=False)
#     version = Column(String, nullable=True)
#     recordsVersion = Column(String, nullable=True)

#     group_id = Column(Integer, ForeignKey('groups.id'), nullable=False)
#     group = relationship('Group', back_populates='aggregates')

#     # Many-to-many relationship with Record
#     records = relationship('Record', secondary=aggregate_records, back_populates='aggregates')


if __name__ == "__main__":
    engine = create_engine('sqlite:///:memory:')
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()

    revent1 = RawEvent(id=1, name="Test Raw Event 1")
    session.add(revent1)
    revent2 = RawEvent(id=2, name="Test Raw Event 2")
    session.add(revent2)
    session.commit()



    event1.name
    'Test Raw Event 1'

    event2.name
    'Test Raw Event 2'

    session.query(Event).first().name
    'Test Raw Event 1'
    
    session.query(Event).first().event_name
    1


"""
    step1 = Step(id=1, name="Test Step 1")
    session.add(step1)
    step2 = Step(id=2, name="Test Step 2")
    session.add(step2)
    session.commit()

    print('step name')
    print(step1.name)
    # 'Test Step'

    print('query first')
    print(session.query(Step).first().name)
    # 'Test Step'

    print('query all')
    print([s.name for s in session.query(Step).all()])

    eventFolder1 = EventFolder(id=1, name="Test Event 1", step_id=step1.id)
    session.add(eventFolder1)
    eventFolder2 = EventFolder(id=2, name="Test Event 2", step_id=step1.id)
    session.add(eventFolder2)
    eventFolder3 = EventFolder(id=3, name="Test Event 1", step_id=step2.id)
    session.add(eventFolder3)
    session.commit()

    print('event1 name')
    print(eventFolder1.name)
    #'Test Event 1'

    print(eventFolder2.name)
    #'Test Event 2'

    print(session.query(EventFolder).first().name)
    #'Test Event 1'
    
    print(session.query(EventFolder).first().step_id)
    # 1

    print([(ef.id,ef.name,ef.step_id) for ef in session.query(EventFolder).all()])
    # [('Test Event 1', 1), ('Test Event 2', 1), ('Test Event 1', 2)]

    print([(type(ef).__name__) for ef in session.query(EventFolder).all()])

    print([(type(ef.step).__name__) for ef in session.query(EventFolder).all()])

    events_names = set([ef.name for ef in session.query(EventFolder).all()])
    print(events_names)

    eid = 1
    for event_name in events_names:
        event_steps = [ef.step for ef in session.query(EventFolder).filter(EventFolder.name == event_name).all()]
        event = Event(id=eid,name=event_name,steps=event_steps)
        session.add(event)
        session.commit()
        eid =eid+1

    
    print([(e.id,e.name,[s.name for s in e.steps]) for e in session.query(Event).all()])
    print([(s.id,s.name,[ef.name for ef in s.eventsInStep]) for s in session.query(Step).all()])

    #print[(ef.id,ef.name,ef.step_id,,ef.step) for ef in session.query(EventFolder).all()]

    >>> eventFolder1 = EventFolder(id=1, name="Test Event 1", step_id=step1.id)
    >>> session.add(eventFolder1)
    >>> eventFolder2 = EventFolder(id=2, name="Test Event 2", step_id=step1.id)
    >>> session.add(eventFolder2)
    >>> eventFolder3 = EventFolder(id=3, name="Test Event 1", step_id=step1.id)
    >>> session.add(eventFolder3)
    >>> session.commit()

    >>> eventFolder1.name
    'Test Event 1'

    >>> eventFolder2.name
    'Test Event 2'

    >>> session.query(Event).first().name
    'Test Event 1'
    
    >>> session.query(Event).first().step_id
    1
"""