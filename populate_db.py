from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Step, Event, Group, Record
import os
from db import SessionLocal,init_db
import pandas as pd


from schemas import StepSchema, EventSchema, GroupSchema, RecordSchema

step_schema = StepSchema()
steps_schema = StepSchema(many=True)
event_schema = EventSchema()
events_schema = EventSchema(many=True)
group_schema = GroupSchema()
groups_schema = GroupSchema(many=True)
record_schema = RecordSchema()
records_schema = RecordSchema(many=True)

def get_sub_dirs(path):
    #print('path',path,os.listdir(path))
    subdirs = [x for x in os.listdir(path) if os.path.isdir(path+'/'+x)] #os.walk(path)]
    return subdirs

def get_sub_csvs(path):
    print('path',path,os.listdir(path))
    csvs = [x for x in os.listdir(path) if '.csv' in x] #os.walk(path)]
    return csvs


# Replace 'sqlite:///your_database.db' with your actual database connection string
#DATABASE_URL = "sqlite:///data/data.db"

# Create engine
#engine = create_engine(DATABASE_URL)

# Bind the engine to the metadata of the Base class so that the declaratives can be accessed through a DBSession instance
#Base.metadata.bind = engine

# Create a DBSession instance
#DBSession = sessionmaker(bind=engine)
session = SessionLocal() #DBSession()

init_db()

# Clear existing data from tables
session.query(Step).delete()
session.query(Event).delete()
session.query(Group).delete()
session.query(Record).delete()
session.commit()#

# Create steps
raw = Step(id = 1, name='raw')
proc = Step(id = 2, name='proc')

# Add groups to the session
session.add(raw)
session.add(proc)
session.commit()

#print steps table
steps = session.query(Step).all()

# Convert to pandas DataFrame
step_data = [{'id': step.id, 'name': step.name} for step in steps]
df_steps = pd.DataFrame(step_data)

# Print steps DataFrame
print('--steps--')
print(df_steps)
print('---------')

steps_schema_dump = steps_schema.dump(steps)
print('steps dump', steps_schema_dump)

#get, create and add events 

eid = 1
for sDic in steps_schema_dump:
    sid = sDic['id']
    sname = sDic['name']
    path = f'C:/Users/g_gos/records/{sname}'
    print('path',path)
    if os.path.isdir(path):
        eventsList = get_sub_dirs(path)
        print('events',eventsList)
        for eventName in eventsList:
            event = Event(id = eid,name=eventName, step_id = sid)
            print('created event in raw',event.id,event.name)
            session.add(event)
            eid = eid+1
    else:
        print('error dir does not exist')


session.commit()

#print events table
events = session.query(Event).all()

# Convert to pandas DataFrame
events_data = [{'id': event.id, 'name': event.name, 'step_id': event.step_id} for event in events]
df_events = pd.DataFrame(events_data)

# Print DataFrame
print('--Events--')
print(df_events)
print('---------')

steps_schema_dump = steps_schema.dump(steps)
print('steps dump', steps_schema_dump)

events_schema_dump = events_schema.dump(events)
print('events dump', events_schema_dump)

#get, create and add groups

gid = 1
for sDic in steps_schema_dump:
    sid = sDic['id']
    sname = sDic['name']
    eDics = sDic['events']
    for eDic in eDics:
        eid = eDic['id']
        ename = eDic['name']
        path = f'C:/Users/g_gos/records/{sname}/{ename}'
        print(path)
        if os.path.isdir(path):
            gorupList = get_sub_dirs(path)
            print('groups',gorupList)
            for groupName in gorupList:
                group = Group(id=gid, name=groupName, event_id=eid)
                print('created group',gid,groupName)
                session.add(group)
                gid = gid+1
        else:
            print('error dir does not exist')

session.commit()

#print events table
groups = session.query(Group).all()

# Convert to pandas DataFrame
group_data = [{'id': group.id, 'name': group.name, 'event_id': group.event_id} for group in groups]
df_group = pd.DataFrame(group_data)

# Print DataFrame
print('--Groups--')
print(df_group)
print('---------')

steps_schema_dump = steps_schema.dump(steps)
print('steps dump', steps_schema_dump)

rid = 1
for sDic in steps_schema_dump:
    sid = sDic['id']
    sname = sDic['name']
    eDics = sDic['events']
    for eDic in eDics:
        eid = eDic['id']
        ename = eDic['name']
        gDics = eDic['groups']
        for gDic in gDics:
            gid = gDic['id']
            gname = gDic['name']
            path = f'C:/Users/g_gos/records/{sname}/{ename}/{gname}'
            print(path)
            if os.path.isdir(path):
                recordList = get_sub_csvs(path)
                if len(recordList) > 0:
                    print('record',recordList)
                    for recordName in recordList:
                        record = Record(id=rid, name=recordName, group_id=gid)
                        print('created',rid,recordName)
                        session.add(record)
                        rid = rid+1
                else:
                    verList = get_sub_dirs(path)
                    for ver in verList:
                        print('ver',ver)
                        recordList = get_sub_csvs(path+'/'+ver)
                        for recordName in recordList:
                            record = Record(id=rid, name=recordName, version = ver, group_id=gid)
                            print('created',rid,recordName)
                            session.add(record)
                            rid = rid+1
            else:
                print('error dir does not exist')

session.commit()

#print events table
records = session.query(Record).all()

# Convert to pandas DataFrame
record_data = [{'id': record.id, 'name': record.name, 'group_id': record.group_id} for record in records]
df_record = pd.DataFrame(record_data)

# Print DataFrame
print('--Records--')
print(df_record)
print('---------')

steps_schema_dump = steps_schema.dump(steps)
print('steps dump', steps_schema_dump)

print("Database populated successfully!")

# Close the session
session.close()