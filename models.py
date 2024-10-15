from sqlalchemy import Column, Integer, Numeric, String, Date, DateTime, ForeignKey, Table, create_engine
from sqlalchemy.orm import relationship, sessionmaker, declarative_base

Base = declarative_base()

# Association table for Aggregate <-> Record
#aggregate_records = Table(
#    'aggregate_records', Base.metadata,
#    Column('aggregate_id', Integer, ForeignKey('aggregates.id')),
#    Column('record_id', Integer, ForeignKey('records.id'))
#)

# Association table for Event <-> Step
#event_steps = Table(
#    'event_step', Base.metadata,
#    Column('step_id', Integer, ForeignKey('steps.id')),
#    Column('event_id', Integer, ForeignKey('events.id'))
#)


class RawEvent(Base):
    """
    Raw event model for managing events with groups of records from acquired raw folser.

    >>> engine = create_engine('sqlite:///:memory:')
    >>> Base.metadata.create_all(engine)
    >>> Session = sessionmaker(bind=engine)
    >>> session = Session()

    >>> revent1 = RawEvent(id=1, name="Test Raw Event 1")
    >>> session.add(revent1)
    >>> revent2 = RawEvent(id=2, name="Test Raw Event 2")
    >>> session.add(revent2)
    >>> session.commit()

    >>> revent1.name
    'Test Raw Event 1'

    >>> revent2.name
    'Test Raw Event 2'

    >>> session.query(RawEvent).first().name
    'Test Raw Event 1'
    """
    __tablename__ = 'rawEvents'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    startDate = Column(Date, nullable=True)
    endDate = Column(Date, nullable=True)
    location = Column(String, nullable=True)
    notes = Column(String, nullable=True)
    path = Column(String, nullable=True)
    rawgroups = relationship('RawGroup', back_populates='rawevent')
    rawrecords = relationship('RawRecord', back_populates='rawevent')


class RawGroup(Base):
    """
    Raw group model for managing groups of records from acquired raw folser.

    >>> engine = create_engine('sqlite:///:memory:')
    >>> Base.metadata.create_all(engine)
    >>> Session = sessionmaker(bind=engine)
    >>> session = Session()

    >>> revent1 = RawEvent(id=1, name="Test Raw Event 1")
    >>> session.add(revent1)
    >>> revent2 = RawEvent(id=2, name="Test Raw Event 2")
    >>> session.add(revent2)
    >>> session.commit()

    >>> rgroup1 = RawGroup(id=1, name="Test Raw Group 1", rawevent_id=revent1.id)
    >>> session.add(rgroup1)
    >>> rgroup2 = RawGroup(id=2, name="Test Raw Group 2", rawevent_id=revent2.id)
    >>> session.add(rgroup2)
    >>> rgroup3 = RawGroup(id=3, name="Test Raw Group 3", rawevent_id=revent1.id)
    >>> session.add(rgroup3)
    >>> rgroup4 = RawGroup(id=4, name="Test Raw Group 4 no envent")
    >>> session.add(rgroup4)
    >>> session.commit()

    >>> rgroup1.name
    'Test Raw Group 1'

    >>> rgroup2.name
    'Test Raw Group 2'

    >>> rgroup4.name
    'Test Raw Group 4 no envent'

    >>> rgroup4.rawevent_id

    >>> session.query(RawGroup).first().name
    'Test Raw Group 1'
    
    >>> session.query(RawGroup).first().rawevent_id
    1

    >>> session.query(RawGroup).first().rawevent.name
    'Test Raw Event 1'

    >>> [re.name for re in session.query(RawEvent).all()]
    ['Test Raw Event 1', 'Test Raw Event 2']

    >>> [[rg.name for rg in re.rawgroups] for re in session.query(RawEvent).all()]
    [['Test Raw Group 1', 'Test Raw Group 3'], ['Test Raw Group 2']]
        
    """
    __tablename__ = 'rawGroups'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    startDate = Column(Date, nullable=True)
    endDate = Column(Date, nullable=True)
    notes = Column(String, nullable=True)
    path = Column(String, nullable=True)
    rawevent_id = Column(Integer, ForeignKey('rawEvents.id'), nullable=True)
    rawevent = relationship('RawEvent', back_populates='rawgroups')

    rawrecords = relationship('RawRecord', back_populates='rawgroup')

    groups = relationship('Group', back_populates='rawgroup')

class RawRecord(Base):
    """
    Raw record model for managing records from groups in acquired raw folser.

    >>> engine = create_engine('sqlite:///:memory:')
    >>> Base.metadata.create_all(engine)
    >>> Session = sessionmaker(bind=engine)
    >>> session = Session()

    >>> revent1 = RawEvent(id=1, name="Test Raw Event 1")
    >>> session.add(revent1)
    >>> revent2 = RawEvent(id=2, name="Test Raw Event 2")
    >>> session.add(revent2)
    >>> session.commit()

    >>> rgroup1 = RawGroup(id=1, name="Test Raw Group 1", rawevent_id=revent1.id)
    >>> session.add(rgroup1)
    >>> rgroup2 = RawGroup(id=2, name="Test Raw Group 2", rawevent_id=revent2.id)
    >>> session.add(rgroup2)
    >>> rgroup3 = RawGroup(id=3, name="Test Raw Group 3", rawevent_id=revent1.id)
    >>> session.add(rgroup3)
    >>> rgroup4 = RawGroup(id=4, name="Test Raw Group 4 no envent")
    >>> session.add(rgroup4)
    >>> session.commit()

    >>> rrecord1 = RawRecord(id=1, name="Test Raw Record 1", rawgroup_id=rgroup1.id, rawevent_id = rgroup1.rawevent_id)
    >>> session.add(rrecord1)
    >>> rrecord2 = RawRecord(id=2, name="Test Raw Record 2", rawgroup_id=rgroup1.id, rawevent_id = rgroup1.rawevent_id)
    >>> session.add(rrecord2)
    >>> rrecord3 = RawRecord(id=3, name="Test Raw Record 3", rawgroup_id=rgroup2.id, rawevent_id = rgroup2.rawevent_id)
    >>> session.add(rrecord3)
    >>> rrecord4 = RawRecord(id=4, name="Test Raw Record 4", rawgroup_id=rgroup3.id, rawevent_id = rgroup3.rawevent_id)
    >>> session.add(rrecord4)
    >>> rrecord5 = RawRecord(id=5, name="Test Raw Record 5 no event", rawgroup_id=rgroup4.id, rawevent_id = rgroup4.rawevent_id)
    >>> session.add(rrecord5)
    >>> session.commit()    

    >>> rrecord1.name
    'Test Raw Record 1'

    >>> rrecord4.name
    'Test Raw Record 4'

    >>> session.query(RawRecord).first().name
    'Test Raw Record 1'
    
    >>> session.query(RawRecord).first().rawgroup_id
    1

    >>> session.query(RawRecord).first().rawgroup.name
    'Test Raw Group 1'

    >>> session.query(RawRecord).first().rawgroup.rawevent.name
    'Test Raw Event 1'

    >>> [rr.name for rr in session.query(RawRecord).all()]
    ['Test Raw Record 1', 'Test Raw Record 2', 'Test Raw Record 3', 'Test Raw Record 4', 'Test Raw Record 5 no event']

    >>> [[rr.name for rr in rg.rawrecords] for rg in session.query(RawGroup).all()]
    [['Test Raw Record 1', 'Test Raw Record 2'], ['Test Raw Record 3'], ['Test Raw Record 4'], ['Test Raw Record 5 no event']]

    >>> session.query(RawRecord).first().rawevent.name
    'Test Raw Event 1'

    >>> [[rr.name for rr in re.rawrecords] for re in session.query(RawEvent).all()]
    [['Test Raw Record 1', 'Test Raw Record 2', 'Test Raw Record 4'], ['Test Raw Record 3']]
        
    """
    __tablename__ = 'rawRecords'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    startTime = Column(DateTime, nullable=True)
    endTime = Column(DateTime, nullable=True)
    totalTime = Column(Numeric, nullable=True)
    totalVariation = Column(Numeric, nullable=True)
    navigationMods = Column(String, nullable=True)
    notes = Column(String, nullable=True)
    path = Column(String, nullable=True)

    rawevent_id = Column(Integer, ForeignKey('rawEvents.id'), nullable=True)
    rawevent = relationship('RawEvent', back_populates='rawrecords')

    rawgroup_id = Column(Integer, ForeignKey('rawGroups.id'), nullable=False)
    rawgroup = relationship('RawGroup', back_populates='rawrecords')

    records = relationship('Record', back_populates='rawrecord')

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
#     #eventsInStep = relationship('EventFolder', back_populates='step')
#     #events = relationship('Event', back_populates='steps')
#     events = relationship('Event', secondary=event_steps, back_populates='steps')

class Event(Base):
    """
    Events model for managing groups of records and aggregates from events.

    >>> engine = create_engine('sqlite:///:memory:')
    >>> Base.metadata.create_all(engine)
    >>> Session = sessionmaker(bind=engine)
    >>> session = Session()

    >>> revent1 = RawEvent(id=1, name="Test Raw Event 1")
    >>> session.add(revent1)
    >>> revent2 = RawEvent(id=2, name="Test Raw Event 2")
    >>> session.add(revent2)
    >>> session.commit()

    >>> event1 = Event(id=1, name="Test Event 1", rawevent_id=revent1.id)
    >>> session.add(event1)
    >>> event2 = Event(id=2, name="Test Event 2", rawevent_id=revent2.id)
    >>> session.add(event2)
    >>> session.commit()

    >>> event1.name
    'Test Event 1'

    >>> event2.name
    'Test Event 2'

    >>> session.query(Event).first().name
    'Test Event 1'
    
    >>> session.query(Event).first().rawevent_id
    1

    >>> session.query(Event).first().rawevent.name
    'Test Raw Event 1'

    >>> session.query(Event).first().rawevent.rawgroups
    []
    """
    __tablename__ = 'events'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    startDate = Column(Date, nullable=True)
    endDate = Column(Date, nullable=True)
    location = Column(String, nullable=True)
    notes = Column(String, nullable=True)
    path = Column(String, nullable=True)
    
    # connections
    rawevent_id = Column(Integer, ForeignKey('rawEvents.id'), nullable=False)
    rawevent = relationship('RawEvent') #, back_populates='event')

    groups = relationship('Group', back_populates='event')

#     #rawPath = Column(String, nullable=True)
#     #rawgroups = relationship('RawGroup', back_populates='rawevent')
#     #rawrecords = relationship('RawRecord', back_populates='rawevent')
    
#     #procPath = Column(String, nullable=True)
#     #aggrPath = Column(String, nullable=True)
    

class Group(Base):
    """
    Group model for managing groups of records and aggregates from events.

    >>> engine = create_engine('sqlite:///:memory:')
    >>> Base.metadata.create_all(engine)
    >>> Session = sessionmaker(bind=engine)
    >>> session = Session()

    >>> revent1 = RawEvent(id=1, name="Test Raw Event 1")
    >>> session.add(revent1)
    >>> revent2 = RawEvent(id=2, name="Test Raw Event 2")
    >>> session.add(revent2)
    >>> session.commit()

    >>> rgroup1 = RawGroup(id=1, name="Test Raw Group 1", rawevent_id=revent1.id)
    >>> session.add(rgroup1)
    >>> rgroup2 = RawGroup(id=2, name="Test Raw Group 2", rawevent_id=revent2.id)
    >>> session.add(rgroup2)
    >>> rgroup3 = RawGroup(id=3, name="Test Raw Group 3", rawevent_id=revent1.id)
    >>> session.add(rgroup3)
    >>> rgroup4 = RawGroup(id=4, name="Test Raw Group 4 no envent")
    >>> session.add(rgroup4)
    >>> session.commit()

    >>> event1 = Event(id=1, name="Test Event 1", rawevent_id=revent1.id)
    >>> session.add(event1)
    >>> event2 = Event(id=2, name="Test Event 2", rawevent_id=revent2.id)
    >>> session.add(event2)
    >>> session.commit()

    >>> group1 = Group(id=1, name="Test Group 1", rawgroup_id=rgroup1.id, event_id=event1.id)
    >>> session.add(group1)
    >>> group2 = Group(id=2, name="Test Group 2", rawgroup_id=rgroup2.id, event_id=event2.id)
    >>> session.add(group2)
    >>> session.commit()

    >>> group1.name
    'Test Group 1'

    >>> group2.name
    'Test Group 2'

    >>> session.query(Group).first().name
    'Test Group 1'
    
    >>> session.query(Group).first().event_id
    1

    >>> session.query(Group).first().event.name
    'Test Event 1'

    >>> [g.name for g in session.query(Group).first().event.groups]
    ['Test Group 1']

    >>> session.query(Group).first().rawgroup_id
    1

    >>> session.query(Group).first().rawgroup.name
    'Test Raw Group 1'

    >>> [rg.name for rg in session.query(Event).first().rawevent.rawgroups]
    ['Test Raw Group 1', 'Test Raw Group 3']

    """
    __tablename__ = 'groups'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    version = Column(String, nullable=True)
    
    startDate = Column(Date, nullable=True)
    endDate = Column(Date, nullable=True)
    notes = Column(String, nullable=True)
    path = Column(String, nullable=True)

    # connections    
    rawgroup_id = Column(Integer, ForeignKey('rawGroups.id'), nullable=False)
    rawgroup = relationship('RawGroup', back_populates='groups')

    event_id = Column(Integer, ForeignKey('events.id'), nullable=False)
    event = relationship('Event', back_populates='groups')
    
    records = relationship('Record', back_populates='group')
#     #aggregates = relationship('Aggregate', back_populates='group')

class Record(Base):
    """
    Group model for managing groups of records and aggregates from events.

    >>> engine = create_engine('sqlite:///:memory:')
    >>> Base.metadata.create_all(engine)
    >>> Session = sessionmaker(bind=engine)
    >>> session = Session()

    >>> revent = RawEvent(id=1, name="Test Raw Event")
    >>> session.add(revent)
    >>> session.commit()

    >>> rgroup = RawGroup(id=1, name="Test Raw Group", rawevent_id=revent.id)
    >>> session.add(rgroup)
    >>> session.commit()

    >>> rrecord = RawRecord(id=1, name="Test Raw Record", rawgroup_id=rgroup.id, rawevent_id = rgroup.rawevent_id)
    >>> session.add(rrecord)
    >>> session.commit()

    >>> event = Event(id=1, name="Test Event", rawevent_id=revent.id)
    >>> session.add(event)
    >>> session.commit()

    >>> group = Group(id=1, name="Test Group", rawgroup_id=rgroup.id, event_id=event.id)
    >>> session.add(group)
    >>> session.commit()
    
    >>> record = Record(id=1, name="Test Record", rawrecord_id=rrecord.id , group_id=group.id)
    >>> session.add(record)
    >>> session.commit()

    >>> record.name
    'Test Record'

    >>> record.rawrecord_id
    1

    >>> record.rawrecord.name
    'Test Raw Record'

    >>> record.group_id
    1

    >>> record.group.name
    'Test Group'

    >>> record.group.event.name
    'Test Event'

    >>> session.query(Group).first().name
    'Test Group'
    
    >>> session.query(Record).first().name
    'Test Record'
    >>> session.query(Record).first().id
    1
    
    >>> session.query(Record).first().group_id
    1
    
    >>> session.query(Record).first().group.name
    'Test Group'
    
    """
    __tablename__ = 'records'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    version = Column(String, nullable=True)

    rawrecord_id = Column(Integer, ForeignKey('rawRecords.id'), nullable=False)
    rawrecord = relationship('RawRecord', back_populates='records')

    group_id = Column(Integer, ForeignKey('groups.id'), nullable=False)
    group = relationship('Group', back_populates='records')
    
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

    rgroup1 = RawGroup(id=1, name="Test Raw Group 1", rawevent_id=revent1.id)
    session.add(rgroup1)
    rgroup2 = RawGroup(id=2, name="Test Raw Group 2", rawevent_id=revent2.id)
    session.add(rgroup2)
    rgroup3 = RawGroup(id=3, name="Test Raw Group 3", rawevent_id=revent1.id)
    session.add(rgroup3)
    rgroup4 = RawGroup(id=4, name="Test Raw Group 4 no envent")
    session.add(rgroup4)
    session.commit()

    print(rgroup4.name)
    'Test Raw Record 1' 
    print(rgroup4.rawevent_id)
    None 

    rrecord1 = RawRecord(id=1, name="Test Raw Record 1", rawgroup_id=rgroup1.id, rawevent_id = rgroup1.rawevent_id)
    session.add(rrecord1)
    rrecord2 = RawRecord(id=2, name="Test Raw Record 2", rawgroup_id=rgroup1.id, rawevent_id = rgroup1.rawevent_id)
    session.add(rrecord2)
    rrecord3 = RawRecord(id=3, name="Test Raw Record 3", rawgroup_id=rgroup2.id, rawevent_id = rgroup2.rawevent_id)
    session.add(rrecord3)
    rrecord4 = RawRecord(id=4, name="Test Raw Record 4", rawgroup_id=rgroup3.id, rawevent_id = rgroup3.rawevent_id)
    session.add(rrecord4)
    rrecord5 = RawRecord(id=5, name="Test Raw Record 5 no event", rawgroup_id=rgroup4.id, rawevent_id = rgroup4.rawevent_id)
    session.add(rrecord5)
    session.commit()

    print(rrecord1.name)
    'Test Raw Record 1'

    print(rrecord4.name)
    'Test Raw Record 4'

    print(session.query(RawRecord).first().name)
    'Test Raw Group 1'
    
    print(session.query(RawRecord).first().rawgroup_id)
    1

    print(session.query(RawRecord).first().rawgroup.name)
    'Test Raw Group 1'

    print(session.query(RawRecord).first().rawgroup.rawevent.name)
    'Test Raw Event 1'

    print([rr.name for rr in session.query(RawRecord).all()])
    ['Test Raw Record 1', 'Test Raw Record 2', 'Test Raw Record 3', 'Test Raw Record 4', 'Test Raw Record 5 no event']

    print([[rr.name for rr in rg.rawrecords] for rg in session.query(RawGroup).all()])
    [['Test Raw Record 1', 'Test Raw Record 2'], ['Test Raw Record 3'], ['Test Raw Record 4'], ['Test Raw Record 5 no event']]

    print(session.query(RawRecord).first().rawevent.name)
    'Test Raw Event 1'

    print([[rr.name for rr in re.rawrecords] for re in session.query(RawEvent).all()])
    [['Test Raw Record 1', 'Test Raw Record 2', 'Test Raw Record 4'], ['Test Raw Record 3']]

    event1 = Event(id=1, name="Test Event 1",rawevent_id=1)
    session.add(event1)
    #event2 = Event(id=2, name="Test Raw Event 2")
    #session.add(event2)
    session.commit()

    print(event1.name)
    print(session.query(Event).first().name)
    print(session.query(Event).first().rawevent_id)
    print(session.query(Event).first().rawevent.name)

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