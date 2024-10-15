from flask import jsonify, request
from db import SessionLocal
from models import Event, Group, Record #, Aggregate
from schemas import EventSchema, GroupSchema #, RecordSchema, AggregateSchema
import pandas as pd

import json
import config
recordsDirs = config.path

#event_schema = EventSchema()
events_schema = EventSchema(many=True, only=('id', 'name','rawevent') )
#group_schema = GroupSchema()
groups_schema = GroupSchema(many=True, only=('id', 'name','rawgroup','event'))
#record_schema = RecordSchema()
#records_schema = RecordSchema(many=True)

#aggregates_schema = AggregateSchema(many=True)


#-----------------------------------------
# API Calls
#---------------------------------

def get_events():
    session = SessionLocal()
    events = session.query(Event).all()
    return jsonify(events_schema.dump(events))
    #return jsonify([{'id': event.id, 'name': event.name} for event in events])

def get_groups():
    session = SessionLocal()
    groups = session.query(Group).all()
    return jsonify(groups_schema.dump(groups))
    #return jsonify([{'id': event.id, 'name': event.name} for event in events])

# def get_event_groups(step_name,event_name):
#     session = SessionLocal()
#     step_id = get_step_id_by_name(session, step_name)
#     print('step_id',step_id)
#     events_id = get_event_id_with_name(session, step_id, event_name)
#     print('event_id',events_id)
#     #groups = session.query(Group).filter(Group.event_id == event_id and Group.step_id == step_id).all()
#     groups = get_groups_by_event_id(session, events_id)
#     #return jsonify(groups_schema.dump(groups))
#     return jsonify([{'id': group.id, 'name': group.name, 'step_id': group.event_id} for group in groups])


# def get_group_records(step_name,event_name,group_name):
#     session = SessionLocal()
#     step_id = get_step_id_by_name(session, step_name)
#     print('step_id',step_id)
#     event_id = get_event_id_with_name(session, step_id, event_name)
#     print('event_id',event_id)
#     group_id = get_group_id_with_name(session, event_id, group_name)
#     print('group_id',group_id)

#     records = get_records_by_group_id(session, group_id) #(session, step_id, event_id, group_id)
#     return jsonify(records_schema.dump(records))

# def get_group_record(step_name,event_name,group_name,version,record_name):
#     tempPath = recordsDirs+ step_name +'/'+ event_name +'/'+ group_name+'/'+version+'/'
#     csvName = tempPath+record_name
#     print(csvName)
#     df = pd.read_csv(csvName)
#     print('df',df)
#     return df.to_json(orient="columns")

# def get_group_aggregates(step_name,event_name,group_name):
#     session = SessionLocal()
#     step_id = get_step_id_by_name(session, step_name)
#     print('step_id',step_id)
#     event_id = get_event_id_with_name(session, step_id, event_name)
#     print('event_id',event_id)
#     group_id = get_group_id_with_name(session, event_id, group_name)
#     print('group_id',group_id)

#     aggregates = get_aggregates_by_group_id(session, group_id) #(session, step_id, event_id, group_id)
#     return jsonify(aggregates_schema.dump(aggregates))

# def get_group_aggregate(step_name,event_name,group_name,aggregate_name):
#     tempPath = recordsDirs+ step_name +'/'+ event_name +'/'+ group_name+'/'
#     with open(tempPath+aggregate_name) as json_file:
#         dicAgg = json.load(json_file)
#     return dicAgg 

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