from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db import SessionLocal,init_db

import os
import pandas as pd
import json
import datetime
import pathlib
from pprint import pprint

from models import Base, RawEvent, RawGroup, RawRecord, Event,  Group, Record #Step, Aggregate
from schemas import RawEventSchema, RawGroupSchema, RawRecordSchema, EventSchema, GroupSchema, RecordSchema #StepSchema


raw_event_schema = RawEventSchema()
raw_events_schema = RawEventSchema(many=True)
raw_groups_schema = RawGroupSchema(many=True)
raw_records_schema = RawRecordSchema(many=True)

events_schema = EventSchema(many=True)
group_schema = GroupSchema()
groups_schema = GroupSchema(many=True)
reocrds_schema = RecordSchema(many=True)

import config
recordsDirs = config.path #'/home/gosti/capturedata/' #'C:/Users/g_gos/Downloads/capturedata/' #config.path #'test/records/'  #'/var/www/html/records/' #'C:/Users/g_gos/records/'

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
session.query(RawEvent).delete()
session.query(RawGroup).delete()
session.query(RawRecord).delete()
#session.query(Step).delete()
session.query(Event).delete()
session.query(Group).delete()
session.query(Record).delete()
#session.query(Aggregate).delete()
#session.commit()#

# -----------
# -- Add Raw Events
# -----------

# form list of dictionaries to dictionary of lists
NDRloc = 'Area territoriale di Ricerca di Roma 1 del Cnr - Strada Provinciale 35d, 9 - 00010, Montelibretti (RM)'
NDRnote = 'I4SCIENCE - Innovation, Imagination, Integration, Impact of Science'
NDRpath = recordsDirs

NDRDic = {'id':1,
          'name': 'NDR', 
          'startDate': '2024-09-27', #datetime.date(2024, 9, 27)
          'endDate': '2024-09-27', #datetime.date(2024, 9, 27),
          'location': NDRloc,
          'notes': NDRnote, 
          'path':NDRpath}


raweventsList = [NDRDic]
raweventsClsList = raw_events_schema.load(raweventsList, session=session)

# Add events to the session
session.add_all(raweventsClsList)
session.commit()

#print events table
rawevents = session.query(RawEvent).all()

# Convert to pandas DataFrame
rawevents_data = raw_events_schema.dump(rawevents) #[{'id': event.id, 'name': event.name, 'path':event.path} for event in events]
df_rawevents = pd.DataFrame(rawevents_data)

# Print DataFrame
print('--Raw Events--')
print(df_rawevents)
print('---------')

# -----------
# -- Add Raw Groups
# -----------


def getRawGroupsList(raweventsList):
    rawgroupsList = [] #{'id':[], 'name':[],'path':[], 'rawevent_id':[]}
    gid = 1
    for re in raweventsList:
        path,eid = re['path'],re['id']
        sDate,eDate = re['startDate'],re['endDate']
        #print(path,eid)
        tempPath = pathlib.Path(path)
        tempGroupList = [f for f in tempPath.iterdir() if f.is_dir()]
        tempGroupList.sort()
        #print(tempGroupList)
        for g in tempGroupList:
            rawgroupsList.append({'id':gid,
                                  'name':g.name, 
                                  'startDate': sDate, 
                                  'endDate': eDate, 
                                  'path':str(g),
                                  'rawevent_id':eid})
            gid = gid + 1
    return rawgroupsList

def printRawGroupsList(rawgroupsList):
    print('print groups')
    for rg in rawgroupsList:
        #print(rg)
        print('- ', rg['name'] ,' ',rg['path'],' /')

rawgroupsList = getRawGroupsList(raweventsList)
printRawGroupsList(rawgroupsList)

rawgroupsClsList = raw_groups_schema.load(rawgroupsList, session=session)
print(rawgroupsClsList)

## Add events to the session
session.add_all(rawgroupsClsList)
session.commit()

#print events table
rawgroups = session.query(RawGroup).all()

# Convert to pandas DataFrame
raw_group_data = raw_groups_schema.dump(rawgroups)
df_raw_group = pd.DataFrame(raw_group_data)

# Print DataFrame
print('--Groups--')
print(df_raw_group)
print('---------')


# -----------
# -- Add Raw Records
# -----------

def addTemRecordsToLists(tempRecordsList, gid, eid, recordsList):
    for recordPath in tempRecordsList:
        rid = len(recordsList)+ 1 # get the number of records id add and increment of one
        tempDic = {'id':rid,
                   'name':recordPath.name,
                   'path':str(recordPath),
                   'rawgroup_id':gid,
                   'rawevent_id':eid}
        recordsList.append(tempDic)
    return recordsList

def getRawRecordsList(rawgroupsList):
    recordsList = [] #{'id':[],'name':[],'path':[], 'rawgroup_id':[]}
    for rg in rawgroupsList:
        gid = rg['id']
        eid = rg['rawevent_id']
        tempPath = pathlib.Path(rg['path'])
        tempRecordsList = [f for f in tempPath.iterdir() if f.is_file() & (f.suffix == '.csv')]
        tempRecordsList.sort()
        recordsList =  addTemRecordsToLists(tempRecordsList,gid,eid,recordsList)                                                    
    return recordsList


def printRecordsList(recordsList):
    print('print records')
    for rr in recordsList :
        print('- ', rr['name'] ,' ',rr['path'],' /')

rawrecordsList = getRawRecordsList(rawgroupsList)
printRecordsList(rawrecordsList)

rawrecordsClsList = raw_records_schema.load(rawrecordsList, session=session)
print(rawrecordsClsList)

## Add records to the session
session.add_all(rawrecordsClsList)
session.commit()

#print records table
rawrecords = session.query(RawRecord).all()

# Convert to pandas DataFrame
raw_record_data = raw_records_schema.dump(rawrecords)
df_raw_record = pd.DataFrame(raw_record_data)

# Print DataFrame
print('--Records--')
print(df_raw_record)
print('---------')



# -----------
# -- Add Events mirrowing Raw Events
# -----------

# get raw events and generate coresponding event table
rawevents = session.query(RawEvent).all()
rawevents_data = raw_events_schema.dump(rawevents) 

for re in rawevents_data:
    re['rawevent_id']=re['id']

eventsClsList = events_schema.load(rawevents_data, session=session)
print([e.name for e in eventsClsList])

## Add events to the session
session.add_all(eventsClsList)
session.commit()


# -----------
# -- Add Groups mirrowing Raw Groups
# -----------

# get raw groups and generate coresponding groups table
rawgroups = session.query(RawGroup).all()
rawgroup_data = raw_groups_schema.dump(rawgroups)

group_data = []
for rg in rawgroup_data:
    #print(rg)
    rg['event_id'] = rg['rawevent_id']
    rg['rawgroup_id']=rg['id']
    #rg['version'] = "Raw"
    del rg['rawevent_id']
    rg['version'] = 'Raw'
    #print(rg)
    group_data.append(rg)

#group_schema.load(rg, session=session)

groupsClsList = groups_schema.load(group_data, session=session)
print([g.name for g in groupsClsList])

## Add events to the session
session.add_all(groupsClsList)
session.commit()

# -----------
# -- Add Records mirrowing Raw Records
# -----------

# get raw records and generate coresponding records table
rawrecords = session.query(RawRecord).all()
rawrecord_data = raw_records_schema.dump(rawrecords)

record_data = []
for rr in rawrecord_data:
    pprint(rr)
    rr['event_id'] = rr['rawevent_id']
    rr['group_id'] = rr['rawgroup_id']
    rr['rawrecord_id']=rr['id']
    del rr['rawevent_id']
    del rR['rawgroup_id']
    rr['version'] = 'Raw'