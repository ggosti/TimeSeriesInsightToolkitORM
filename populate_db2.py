from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db import SessionLocal,init_db

import os
import pandas as pd
import json
import datetime
import pathlib

from models import Base, RawEvent, RawGroup, RawRecord #Step, Event, Group, Record, Aggregate
from schemas import RawEventSchema, RawGroupSchema, RawRecordSchema #StepSchema, EventSchema, GroupSchema, RecordSchema


raw_event_schema = RawEventSchema()
raw_events_schema = RawEventSchema(many=True)
raw_groups_schema = RawGroupSchema(many=True)
raw_records_schema = RawRecordSchema(many=True)


import config
recordsDirs = '/home/gosti/capturedata/' #'C:/Users/g_gos/Downloads/capturedata/' #config.path #'test/records/'  #'/var/www/html/records/' #'C:/Users/g_gos/records/'

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
#session.query(Event).delete()
#session.query(Group).delete()
#session.query(Record).delete()
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

def addTemRecordsToLists(tempRecordsList, gid, recordsList):
    for recordPath in tempRecordsList:
        rid = len(recordsList)+ 1 # get the number of records id add and increment of one
        tempDic = {'id':rid,
                   'name':recordPath.name,
                   'path':str(recordPath),
                   'rawgroup_id':gid}
        recordsList.append(tempDic)
    return recordsList

def getRawRecordsList(rawgroupsList):
    recordsList = [] #{'id':[],'name':[],'path':[], 'rawgroup_id':[]}
    for rg in rawgroupsList:
        gid = rg['id']
        tempPath = pathlib.Path(rg['path'])
        tempRecordsList = [f for f in tempPath.iterdir() if f.is_file() & (f.suffix == '.csv')]
        tempRecordsList.sort()
        recordsList =  addTemRecordsToLists(tempRecordsList,gid,recordsList)                                                    
    return recordsList


def printRecordsList(recordsList):
    print('print records')
    for rr in recordsList :
        print('- ', rr['name'] ,' ',rr['path'],' /')

rawrecordsList = getRawRecordsList(rawgroupsList)
printRecordsList(rawrecordsList)

rawrecordsClsList = raw_records_schema.load(rawrecordsList, session=session)
print(rawrecordsClsList)

## Add events to the session
session.add_all(rawrecordsClsList)
session.commit()

#print events table
rawrecords = session.query(RawRecord).all()

# Convert to pandas DataFrame
raw_record_data = raw_records_schema.dump(rawrecords)
df_raw_record = pd.DataFrame(raw_record_data)

# Print DataFrame
print('--Records--')
print(df_raw_record)
print('---------')