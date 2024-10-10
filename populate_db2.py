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


events_schema = RawEventSchema(many=True)
groups_schema = RawGroupSchema(many=True)
records_schema = RawRecordSchema(many=True)


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
def makeRawEventsDic(listEvDic):
    eventsDic = {k:[] for k in NDRDic.keys()}
    for eDic in listEvDic:
        for k in NDRDic.keys():
            eventsDic[k].append(eDic[k])
    return eventsDic

def printRawEvents(eventsDic):
    listKeys = list(eventsDic.keys())
    listValuesList = [eventsDic[k]  for k in listKeys]
    for vals in zip(*listValuesList):
        print('- ', vals)

NDRloc = 'Area territoriale di Ricerca di Roma 1 del Cnr - Strada Provinciale 35d, 9 - 00010, Montelibretti (RM)'
NDRnote = 'I4SCIENCE - Innovation, Imagination, Integration, Impact of Science'
NDRpath = pathlib.Path('C:/Users/g_gos/Downloads/capturedata/')
NDRDic = {'id':1,'name': 'NDR', 'startdate':datetime.date(2024, 9, 27),'endDate':datetime.date(2024, 9, 27),'location': NDRloc,'note': NDRnote, 'path':NDRpath}

raweventsDic = makeRawEventsDic([NDRDic])
printRawEvents(raweventsDic)

# -----------
# -- Add Raw Groups
# -----------

def getRawGroups(paths,raweventsIdList):
    rawgroupsDic = {'id':[], 'name':[],'path':[], 'rawevent_id':[]}
    gid = 1
    for path,eid in zip(paths,raweventsIdList):
        #print(path,eid)
        tempPath = path
        tempGroupList = [f for f in tempPath.iterdir() if f.is_dir()]
        tempGroupList.sort()
        #print(tempGroupList)
        for g in tempGroupList:
            rawgroupsDic['id'].append(gid)
            rawgroupsDic['name'].append(g.name)
            rawgroupsDic['path'].append(g)
            rawgroupsDic['rawevent_id'].append(eid)
            gid = gid + 1
    return rawgroupsDic

def printRawGroups(groupsDic):
    print('print groups')
    for g,p in zip(groupsDic['name'],groupsDic['path']):
        print('- ', g ,' ',p,' /')

rawgroupsDic = getRawGroups(raweventsDic['path'],raweventsDic['id'])
printRawGroups(rawgroupsDic)

# -----------
# -- Add Raw Records
# -----------

def addTemRecordsToLists(tempRecordsList, gid, recordsDic):
    for recordPath in tempRecordsList:
        rid = len(recordsDic['id'])+ 1 # get the number of records id add and increment of one
        recordsDic['id'].append(rid)
        recordsDic['name'].append(recordPath.name)
        recordsDic['path'].append(recordPath)
        recordsDic['rawgroup_id'].append(gid)
    return recordsDic

def getRecords(paths,rawgroupsIdList):
    recordsDic = {'id':[],'name':[],'path':[], 'rawgroup_id':[]}
    for path,gid in zip(paths,rawgroupsIdList):
        tempPath = path
        tempRecordsList = [f for f in tempPath.iterdir() if f.is_file() & (f.suffix == '.csv')]
        tempRecordsList.sort()
        recordsDic =  addTemRecordsToLists(tempRecordsList,gid,recordsDic)                                                    
    return recordsDic


def printRecords(recordsDic):
    print('print records')
    for r,p in zip( recordsDic['name'], recordsDic['path'] ):
        print('- ', r ,' ',p,' /')

recordsDic = getRecords(rawgroupsDic['path'],rawgroupsDic['id'])
printRecords(recordsDic)

# -----------
# Create Raw Events table
# -----------
#{'id':1,'name': 'NDR', 'startdate':datetime.date(2024, 9, 27),'endDate':datetime.date(2024, 9, 27),'location': NDRloc,'note': NDRnote, 'path':NDRpath}

raweventsClsList = [RawEvent(id = i, name=e) for i, e in zip( raweventsDic['id'], raweventsDic['name'] )] # usa meglio raweventsDic per fare dump!!

# Add events to the session
session.add_all(raweventsClsList)
session.commit()

#print events table
events = session.query(RawEvent).all()

# Convert to pandas DataFrame
rawevents_data = [{'id': event.id, 'name': event.name, 'path':event.path} for event in events]
df_rawevents = pd.DataFrame(rawevents_data)

# Print DataFrame
print('--Raw Events--')
print(df_rawevents)
print('---------')