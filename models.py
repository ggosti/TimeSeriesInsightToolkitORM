from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

class Step(Base):
    __tablename__ = 'steps'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    events = relationship('Event', back_populates='step')

class Event(Base):
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

class Record(Base):
    __tablename__ = 'records'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    version = Column(String, nullable=True)
    group_id = Column(Integer, ForeignKey('groups.id'), nullable=False)
    group = relationship('Group', back_populates='records')