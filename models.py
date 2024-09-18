from sqlalchemy import Column, Integer, String, ForeignKey, Table, create_engine
from sqlalchemy.orm import relationship, sessionmaker, declarative_base

Base = declarative_base()

# Association table for Aggregate <-> Record
aggregate_records = Table(
    'aggregate_records', Base.metadata,
    Column('aggregate_id', Integer, ForeignKey('aggregates.id')),
    Column('record_id', Integer, ForeignKey('records.id'))
)

class Step(Base):
    """
    Steps model for managing groups of records and aggregates from events.

    >>> engine = create_engine('sqlite:///:memory:')
    >>> Base.metadata.create_all(engine)
    >>> Session = sessionmaker(bind=engine)
    >>> session = Session()

    >>> step = Step(id=1, name="Test Step")
    >>> session.add(step)
    >>> session.commit()

    >>> step.name
    'Test Step'

    >>> session.query(Step).first().name
    'Test Step'
    """
    __tablename__ = 'steps'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    events = relationship('Event', back_populates='step')

class Event(Base):
    """
    Events model for managing groups of records and aggregates from events.

    >>> engine = create_engine('sqlite:///:memory:')
    >>> Base.metadata.create_all(engine)
    >>> Session = sessionmaker(bind=engine)
    >>> session = Session()

    >>> step = Step(id=1, name="Test Step")
    >>> session.add(step)
    >>> session.commit()

    >>> event1 = Event(id=1, name="Test Event 1", step_id=step.id)
    >>> session.add(event1)
    >>> event2 = Event(id=2, name="Test Event 2", step_id=step.id)
    >>> session.add(event2)
    >>> session.commit()

    >>> event1.name
    'Test Event 1'

    >>> event2.name
    'Test Event 2'

    >>> session.query(Event).first().name
    'Test Event 1'
    
    >>> session.query(Event).first().step_id
    1
    """
    __tablename__ = 'events'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    step_id = Column(Integer, ForeignKey('steps.id'), nullable=False)
    step = relationship('Step', back_populates='events')
    groups = relationship('Group', back_populates='event')

class Group(Base):
    __tablename__ = 'groups'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    event_id = Column(Integer, ForeignKey('events.id'), nullable=False)
    event = relationship('Event', back_populates='groups')
    records = relationship('Record', back_populates='group')
    aggregates = relationship('Aggregate', back_populates='group')

class Record(Base):
    __tablename__ = 'records'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    version = Column(String, nullable=True)
    group_id = Column(Integer, ForeignKey('groups.id'), nullable=False)
    
    # Relationship to Group and Aggregate
    group = relationship('Group', back_populates='records')
    aggregates = relationship('Aggregate', secondary=aggregate_records, back_populates='records')


class Aggregate(Base):
    __tablename__ = 'aggregates'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    version = Column(String, nullable=True)

    group_id = Column(Integer, ForeignKey('groups.id'), nullable=False)
    group = relationship('Group', back_populates='aggregates')

    # Many-to-many relationship with Record
    records = relationship('Record', secondary=aggregate_records, back_populates='aggregates')


