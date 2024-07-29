from flask import jsonify, request
from db import SessionLocal
from models import Step, Event, Group, Record
from schemas import StepSchema, EventSchema, GroupSchema, RecordSchema
import pandas as pd

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

def get_event_id_with_name(session, step_id, event_name):
    #print(session.query(Event).all())
    event = session.query(Event).filter_by(step_id=step_id).filter_by(name=event_name).first()
    #print(events)
    return event.id if event else None

def get_group_id_with_name(session, event_id, group_name):
    group = session.query(Group).filter_by(event_id=event_id).filter_by(name=group_name).first()
    return group.id if group else None


def get_groups_by_event_id(session, event_id):
    groups = session.query(Group).all()
    print('Group')
    # Convert to pandas DataFrame
    group_data = [{'id': group.id, 'name': group.name, 'event_id': group.event_id} for group in groups]
    df_group = pd.DataFrame(group_data)

    # Print DataFrame
    print('--Groups--')
    print(df_group)
    print('---------')

    # print('Join Group and Events')
    # groups_with_events = session.query(Group).join(Event).all()
    # # Print the results
    # #for group in groups_with_events:
    # #    print(f"Group ID: {group.id}, Group Name: {group.name}, Event ID: {group.event_id}, Event Name: {group.event.name}")
    # # Convert to pandas DataFrame
    # group_data = [{'id': group.id, 'name': group.name, 'event_id': group.event_id,  'event_name':group.event.name, 'step_id': group.event.step_id} for group in groups_with_events]
    # df_group = pd.DataFrame(group_data)

    # # Print DataFrame
    # print('--Groups--')
    # print(df_group)
    # print('---------')
    # return session.query(Group).join(Event).filter(Event.step_id == step_id, Group.event_id == event_id).all()
    return session.query(Group).filter(Group.event_id == event_id).all()

def get_records_by_group_id(session, group_id):
    return session.query(Record).filter(Record.group_id == group_id).all()


#-----------------------------------------
# API Calls
#---------------------------------


def get_steps():
    session = SessionLocal()
    steps = session.query(Step).all()
    #return jsonify(steps_schema.dump(steps))
    return jsonify([{'id': step.id, 'name': step.name} for step in steps]) #steps_schema.dump(steps))


def get_step_events(step_name):
    print('step_name',step_name)
    session = SessionLocal()
    #step = session.query(Step).filter(Step.name == step_name).all()
    #print(step[0],step[0].id)
    step_id = get_step_id_by_name(session, step_name)
    print('step_id',step_id)
    events = session.query(Event).filter(Event.step_id == step_id).all()
    #return jsonify(events_schema.dump(events))
    return jsonify([{'id': event.id, 'name': event.name, 'step_id': event.step_id} for event in events])

def get_event_groups(step_name,event_name):
    session = SessionLocal()
    step_id = get_step_id_by_name(session, step_name)
    print('step_id',step_id)
    events_id = get_event_id_with_name(session, step_id, event_name)
    print('event_id',events_id)
    #groups = session.query(Group).filter(Group.event_id == event_id and Group.step_id == step_id).all()
    groups = get_groups_by_event_id(session, events_id)
    #return jsonify(groups_schema.dump(groups))
    return jsonify([{'id': group.id, 'name': group.name, 'step_id': group.event_id} for group in groups])


def get_group_records(step_name,event_name,group_name):
    session = SessionLocal()
    step_id = get_step_id_by_name(session, step_name)
    print('step_id',step_id)
    event_id = get_event_id_with_name(session, step_id, event_name)
    print('event_id',event_id)
    group_id = get_group_id_with_name(session, event_id, group_name)
    print('group_id',group_id)

    records = get_records_by_group_id(session, group_id) #(session, step_id, event_id, group_id)
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