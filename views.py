from flask import jsonify, request
from db import SessionLocal
from models import Step, Event, Group, Record
from schemas import StepSchema, EventSchema, GroupSchema, RecordSchema

step_schema = StepSchema()
steps_schema = StepSchema(many=True)
event_schema = EventSchema()
events_schema = EventSchema(many=True)
group_schema = GroupSchema()
groups_schema = GroupSchema(many=True)
record_schema = RecordSchema()
records_schema = RecordSchema(many=True)

def get_step_id_by_name(session, step_name):
    step = session.query(Step).filter_by(name=step_name).first()
    return step.id if step else None

def get_steps():
    session = SessionLocal()
    steps = session.query(Step).all()
    return jsonify(steps_schema.dump(steps))

def get_step_events(step_name):
    print('step_name',step_name)
    session = SessionLocal()
    #step = session.query(Step).filter(Step.name == step_name).all()
    #print(step[0],step[0].id)
    step_id = get_step_id_by_name(session, step_name)
    print('step_id',step_id)
    events = session.query(Event).filter(Event.step_id == step_id).all()
    return jsonify(events_schema.dump(events))

def get_event_groups(event_id):
    session = SessionLocal()
    groups = session.query(Group).filter(Group.event_id == event_id).all()
    return jsonify(groups_schema.dump(groups))

def get_group_records(group_id):
    session = SessionLocal()
    records = session.query(Record).filter(Record.group_id == group_id).all()
    return jsonify(records_schema.dump(records))

# def create_step():
#     data = request.json
#     session = SessionLocal()
#     step = Step(name=data['name'])
#     session.add(step)
#     session.commit()
#     return step_schema.dump(step), 201

# def create_event(step_id):
#     data = request.json
#     session = SessionLocal()
#     event = Event(name=data['name'], step_id=step_id)
#     session.add(event)
#     session.commit()
#     return event_schema.dump(event), 201

# def create_group(event_id):
#     data = request.json
#     session = SessionLocal()
#     group = Group(name=data['name'], event_id=event_id)
#     session.add(group)
#     session.commit()
#     return group_schema.dump(group), 201

# def create_record(group_id):
#     data = request.json
#     session = SessionLocal()
#     record = Record(name=data['name'], group_id=group_id)
#     session.add(record)
#     session.commit()
#     return record_schema.dump(record), 201