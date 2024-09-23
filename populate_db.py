from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Step, Event, Group, Record, Aggregate
import os
from db import SessionLocal,init_db
import pandas as pd
import json


from schemas import StepSchema, EventSchema, GroupSchema, RecordSchema

#step_schema = StepSchema()
steps_schema = StepSchema(many=True)
#event_schema = EventSchema()
events_schema = EventSchema(many=True)
#group_schema = GroupSchema()
groups_schema = GroupSchema(many=True)
#record_schema = RecordSchema()
#records_schema = RecordSchema(many=True)

def get_sub_dirs(path):
    #print('path',path,os.listdir(path))
    subdirs = [x for x in os.listdir(path) if os.path.isdir(path+'/'+x)] #os.walk(path)]
    subdirs.sort()
    return subdirs

def get_sub_csvs(path):
    #print('path',path,os.listdir(path))
    csvs = [x for x in os.listdir(path) if '.csv' in x] #os.walk(path)]
    return csvs

def get_sub_json(path):
    #print('path',path,os.listdir(path))
    jsons = [x for x in os.listdir(path) if '.json' in x] #os.walk(path)]
    #print(jsons)
    return jsons


import config
recordsDirs = config.path #'test/records/'  #'/var/www/html/records/' #'C:/Users/g_gos/records/'

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
session.query(Aggregate).delete()
session.commit()#

# -----------
# -- Steps:
# -----------

def getSteps(path):
    stepsDic = {'id':[1,2],'name':['raw','proc']}
    return stepsDic #get_sub_dirs(path)

def printSteps():
    print('print steps')
    for s in stepsDic['name']:
        print('- ', s , ' /')

stepsDic = getSteps(recordsDirs)
printSteps()

# -----------
# -- Events
# -----------

def getEvents(path,stepIdList,stepsList):
    eventsDic = {'id':[], 'name':[],'path':[], 'step_id':[]}
    i = 1
    for sid,s in zip(stepIdList,stepsList):
        #print(sid,s)
        tempPath = path+s+'/'
        tempEventList = get_sub_dirs(tempPath)
        for e in tempEventList:
            eventsDic['id'].append(i)
            eventsDic['name'].append(e)
            eventsDic['path'].append(tempPath)
            eventsDic['step_id'].append(sid)
            i = i+1
    return eventsDic

def printEvents(eventsDic):
    print('print events')
    for e,p in zip(eventsDic['name'],eventsDic['path']):
        print('- ', e ,' ',p,' /')

eventsDic = getEvents(recordsDirs,stepsDic['id'],stepsDic['name'])
printEvents(eventsDic)

# -----------
# -- Groups
# -----------

def getGroups(paths,eventsIdList,eventsList):
    groupsDic = {'id':[], 'name':[],'path':[], 'event_id':[]}
    gid = 1
    for p,eid,e in zip(paths,eventsIdList,eventsList):
        tempPath = p+e+'/'
        tempGroupList = get_sub_dirs(tempPath)
        for g in tempGroupList:
            groupsDic['id'].append(gid)
            groupsDic['name'].append(g)
            groupsDic['path'].append(tempPath)
            groupsDic['event_id'].append(eid)
            gid = gid + 1
    return groupsDic

def printGroups(groupsDic):
    print('print groups')
    for g,p in zip(groupsDic['name'],groupsDic['path']):
        print('- ', g ,' ',p,' /')

groupsDic = getGroups(eventsDic['path'],eventsDic['id'],eventsDic['name'])
printGroups(groupsDic)

# -----------
# -- Records
# -----------

def addTemRecordsToLists(tempRecordsList, tempPath, ver, gid, recordsDic):
    for recordName in tempRecordsList:
        rid = len(recordsDic['id'])+ 1 # get the number of records id add and increment of one
        recordsDic['id'].append(rid)
        recordsDic['name'].append(recordName)
        recordsDic['path'].append(tempPath)
        recordsDic['ver'].append(ver)
        recordsDic['group_id'].append(gid)
    return recordsDic

def getRecords(paths,groupsIdList,groupsList):
    recordsDic = {'id':[],'name':[],'path':[],'ver':[],'group_id':[]}
    for p,gid,g in zip(paths,groupsIdList,groupsList):
        tempPath = p+g+'/'
        if os.path.isdir(tempPath):
            tempRecordsList = get_sub_csvs(tempPath)
            if len(tempRecordsList) > 0:
                #print('record',tempRecordsList)
                recordsDic =  addTemRecordsToLists(tempRecordsList,tempPath,None,gid,recordsDic)
            else:
                versList = get_sub_dirs(tempPath)
                for ver in versList:
                    #print('ver',ver)
                    tempRecordsList = get_sub_csvs(tempPath+'/'+ver)
                    recordsDic =  addTemRecordsToLists(tempRecordsList,tempPath,ver,gid,recordsDic)                                                    
        else:
            print('error dir does not exist')
    return recordsDic


def printRecords(recordsDic):
    print('print records')
    for r,p,v in zip( recordsDic['name'], recordsDic['path'], recordsDic['ver'] ):
        print('- ', r ,' ',p,' ',v,' /')

recordsDic = getRecords(groupsDic['path'],groupsDic['id'],groupsDic['name'])
printRecords(recordsDic)

# -----------
# -- Aggregates
# -----------

def getVersionFromRecordFolder(recodsFolder):
    recordsVer = recodsFolder.split("/")[-1]
    if len(recordsVer) == 0:
        recordsVer = recodsFolder.split("/")[-2]    
    return recordsVer

def addTemAggregatesToLists(tempAggList,tempPath, gid, aggregatesDic):
    for aggName in tempAggList:
        if not 'pars.json' in aggName:
            with open(tempPath+'/'+aggName) as json_file:
                dicAgg = json.load(json_file)
            recordsList = None
            if 'records' in dicAgg:
                recordsList = dicAgg['records']
                recordsVer = getVersionFromRecordFolder(dicAgg["records folder"])
                #print('recordsVer', recordsVer)
            aid = len(aggregatesDic['id'])+ 1 # get the number of records id add and increment of one
            aggregatesDic['id'].append(aid)
            aggregatesDic['name'].append(aggName)
            aggregatesDic['path'].append(tempPath)
            aggregatesDic['ver'].append(None)
            aggregatesDic['recordsVer'].append(recordsVer)
            aggregatesDic['records'].append(recordsList)
            aggregatesDic['group_id'].append(gid)
    #print('aggeregatesRegVerList',aggregateDic['recordsVer'])
    return aggregatesDic


def getAggregates(paths,groupsIdList,groupsList):
    aggregateDic = {'id':[],'name':[],'path':[],'ver':[],'recordsVer':[],'records':[],'group_id':[]}
    for p,gid,g in zip(paths,groupsIdList,groupsList):
        tempPath = p+g+'/'
        if os.path.isdir(tempPath):
            tempAggList = get_sub_json(tempPath)
            if len(tempAggList) > 0:
                aggregateDic = addTemAggregatesToLists(tempAggList,tempPath,gid,aggregateDic)
            else:
                print('error aggregate json does not exist')
        else:
            print('error dir does not exist for aggregate json')
    return aggregateDic


def printAggregates(aggregatesDic):
    print('print aggreagare')
    for a,p,recVer, recs in zip( aggregatesDic['name'], aggregatesDic['path'], aggregatesDic['recordsVer'], aggregatesDic['records']):
        try:
            print('- ', a ,' ',p,' ',recVer, recs[:3])
        except TypeError:
            print('- ', a ,' ',p,' ',recVer)
            print('ERROR!!!: TyperError for recods',recs)

aggregatesDic = getAggregates(groupsDic['path'],groupsDic['id'],groupsDic['name'])
printAggregates(aggregatesDic)

# -----------
# Create steps
# -----------

stepsClsList = [Step(id = i, name=s) for i,s in zip(stepsDic['id'],stepsDic['name'])]

# Add steps to the session
session.add_all(stepsClsList)
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

# -----------
# Create Events
# -----------

eventsClsList = [Event(id = i, name=e, step_id=sid) for i, e, sid in zip( eventsDic['id'], eventsDic['name'], eventsDic['step_id'] )]

# Add events to the session
session.add_all(eventsClsList)
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

# -----------
# Create Groups
# -----------

groupsClsList = [Group(id = i, name=g, event_id=eid) for i, g, eid in zip( groupsDic['id'], groupsDic['name'], groupsDic['event_id'] )]

# Add groups to the session
session.add_all(groupsClsList)
session.commit()

#query groups table
groups = session.query(Group).all()

# Convert to pandas DataFrame
group_data = [{'id': group.id, 'name': group.name, 'event_id': group.event_id} for group in groups]
df_group = pd.DataFrame(group_data)

# Print DataFrame
print('--Groups--')
print(df_group)
print('---------')

# -----------
# Create Records
# -----------
recordsClsList = [Record(id = i, name=g, version=v , group_id=gid) for i, g, v, gid in zip( recordsDic['id'], recordsDic['name'], recordsDic['ver'], recordsDic['group_id'] )]

# Add records to the session
session.add_all(recordsClsList)
session.commit()

#print records table
records = session.query(Record).all()

# Convert to pandas DataFrame
record_data = [{'id': record.id, 'name': record.name, 'version':record.version, 'group_id': record.group_id} for record in records]
df_record = pd.DataFrame(record_data)

# Print DataFrame
print('--Records--')
print(df_record)
print('---------')

# -----------
# Create Aggregates
# -----------

aggregatesClsList = []

for i, a, ver, rVer, rs, gid in zip( aggregatesDic['id'], 
                                        aggregatesDic['name'], 
                                        aggregatesDic['ver'],
                                        aggregatesDic['recordsVer'],
                                        aggregatesDic['records'],
                                        aggregatesDic['group_id'] ):
    #print('gid',gid)
    #print('rs',rs,'recods',[[record.name,record.name.split('.')[0],record.group_id] for record in records])
    recordsClMap = {(record.name.split('.')[0],record.version,record.group_id):record for record in records}
    #print('record class map')
    #for k,v in recordsClMap.items():
    #    print(k,':', v)
    #    print( (rs[0],rVer,gid) == k, rs[0] == k[0], rVer == k[1], gid == k[2])
    print(i, a, ver, rVer, rs, gid)
    for r in rs:
        print(recordsClMap[(r,rVer,gid)] )
    #aggRecordsCl = [record for record in records if record.name + '.csv' in rs]
    aggTemp = Aggregate(id = i, 
                name=a,
                version = ver,
                recordsVersion = rVer,
                records = [recordsClMap[(r,rVer,gid)]  for r in rs],
                group_id = gid) 
    aggregatesClsList.append(aggTemp)
                

# Add records to the session
session.add_all(aggregatesClsList)
session.commit()

#print events table
aggregates = session.query(Aggregate).all()

# Convert to pandas DataFrame
aggregates_data = [{'id': aggregate.id, 'name': aggregate.name, 'records':aggregate.records, 'group_id': aggregate.group_id} for aggregate in aggregates]
df_aggregate = pd.DataFrame(aggregates_data)

# Print DataFrame
print('--Aggregate--')
print(df_aggregate)
print('---------')

print("Database populated successfully!")

# Close the session
session.close()

"""

session.commit()

#print events table
aggregates = session.query(Aggregate).all()

# Convert to pandas DataFrame
aggregates_data = [{'id': aggregate.id, 'name': aggregate.name, 'records':aggregate.records, 'group_id': aggregate.group_id} for aggregate in aggregates]
df_aggregate = pd.DataFrame(aggregates_data)

# Print DataFrame
print('--Aggregate--')
print(df_aggregate)
print('---------')

print("Database populated successfully!")

# Close the session
session.close()

"""