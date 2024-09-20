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
    print('path',path,os.listdir(path))
    csvs = [x for x in os.listdir(path) if '.csv' in x] #os.walk(path)]
    return csvs

def get_sub_json(path):
    print('path',path,os.listdir(path))
    jsons = [x for x in os.listdir(path) if '.json' in x] #os.walk(path)]
    print(jsons)
    return jsons


recordsDirs = 'test/records/'  #'/var/www/html/records/' #'C:/Users/g_gos/records/'

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

def getSteps(path):
    return ['raw','proc'] #get_sub_dirs(path)

def getEvents(path,stepsList):
    eventsList = []
    eventsPathList = []
    for s in stepsList:
        tempPath = path+s+'/'
        tempEventList = get_sub_dirs(tempPath)
        for e in tempEventList:
            eventsList.append(e)
            eventsPathList.append(tempPath)
    return eventsList,eventsPathList

def getGroups(paths,eventsList):
    groupsList = []
    groupsPathList = []
    for p,e in zip(paths,eventsList):
        tempPath = p+e+'/'
        tempGroupList = get_sub_dirs(tempPath)
        for g in tempGroupList:
            groupsList.append(g)
            groupsPathList.append(tempPath)
    return groupsList,groupsPathList

def addTemRecordsToLists(tempRecordsList,tempPath,recodsList,recordsPathList,recordsVerList):
    for recordName in tempRecordsList:
        recodsList.append(recordName)
        recordsPathList.append(tempPath)
        recordsVerList.append(None)
    return recodsList,recordsPathList,recordsVerList

def getRecords(paths,groupsList):
    recodsList = []
    recordsPathList = []
    recordsVerList = []
    for p,g in zip(paths,groupsList):
        tempPath = p+g+'/'
        if os.path.isdir(tempPath):
            tempRecordsList = get_sub_csvs(tempPath)
            if len(tempRecordsList) > 0:
                #print('record',tempRecordsList)
                recodsList,recordsPathList,recordsVerList =  addTemRecordsToLists(tempRecordsList,tempPath,
                                                                                  recodsList,recordsPathList,recordsVerList)
            else:
                versList = get_sub_dirs(tempPath)
                for ver in versList:
                    #print('ver',ver)
                    tempRecordsList = get_sub_csvs(tempPath+'/'+ver)
                    recodsList,recordsPathList,recordsVerList =  addTemRecordsToLists(tempRecordsList,tempPath,
                                                                                      recodsList,recordsPathList,recordsVerList)
        else:
            print('error dir does not exist')
    return recodsList, recordsPathList, recordsVerList


def getVersionFromRecordFolder(recodsFolder):
    recordsVer = recodsFolder.split("/")[-1]
    if len(recordsVer) == 0:
        recordsVer = recodsFolder.split("/")[-2]    
    return recordsVer


def addTemAggregatesToLists(tempAggList,tempPath, aggeregatesList,aggeregatesPathList,aggeregatesVerList,aggeregatesRegVerList):
    for aggName in tempAggList:
        with open(tempPath+'/'+aggName) as json_file:
            dicAgg = json.load(json_file)
        recordsList = None
        if 'records' in dicAgg:
            recordsList = dicAgg['records']
            recordsVer = getVersionFromRecordFolder(dicAgg["records folder"])
            print('recordsVer', recordsVer)
        aggeregatesList.append(aggName)
        aggeregatesPathList.append(tempPath)
        aggeregatesVerList.append(None)
        aggeregatesRegVerList.append(recordsVer)
    print('aggeregatesRegVerList',aggeregatesRegVerList)
    return aggeregatesList,aggeregatesPathList,aggeregatesVerList,aggeregatesRegVerList


def getAggregates(paths,groupsList,recodsList):
    aggeregatesList = []
    aggeregatesPathList = []
    aggeregatesVerList = []
    aggeregatesRegVerList = []
    for p,g in zip(paths,groupsList):
        tempPath = p+g+'/'
        if os.path.isdir(tempPath):
            tempAggList = get_sub_json(tempPath)
            if len(tempAggList) > 0:
                [aggeregatesList,
                aggeregatesPathList,
                aggeregatesVerList,
                aggeregatesRegVerList] = addTemAggregatesToLists(tempAggList,tempPath,
                                                                aggeregatesList,aggeregatesPathList,aggeregatesVerList,aggeregatesRegVerList)
            else:
                print('error dir does not exist')
        else:
            print('error dir does not exist')
    return aggeregatesList, aggeregatesPathList, aggeregatesVerList, aggeregatesRegVerList

stepsList = getSteps(recordsDirs)
eventsList,eventsPathList = getEvents(recordsDirs,stepsList)
groupsList,groupsPathList = getGroups(eventsPathList,eventsList)
recodsList, recordsPathList, recordsVerList = getRecords(groupsPathList,groupsList)
aggeregatesList, aggeregatesPathList, aggeregatesVerList, aggeregatesRegVerList = getAggregates(groupsPathList,groupsList,recodsList,recordsVerList)

print('print steps')
for s in stepsList:
    print('- ', s , ' /')

print('print events')
for e,p in zip(eventsList,eventsPathList ):
    print('- ', e ,' ',p,' /')

print('print groups')
for g,p in zip(groupsList,groupsPathList ):
    print('- ', g ,' ',p,' /')

print('print records')
for r,p,v in zip( recodsList, recordsPathList, recordsVerList ):
    print('- ', r ,' ',p,' ',v,' /')

print('print aggreagare')
for a,p,regVer in zip( aggeregatesList, aggeregatesPathList, aggeregatesRegVerList ):
    print('- ', a ,' ',p,' ',regVer,' /')
    

"""
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
stepIdMap = {sDic['id']:sDic['name'] for sDic in steps_schema_dump}
print('steps dump')
for s in steps_schema_dump:
    print(s)


#get, create and add events 

eid = 1
for sDic in steps_schema_dump:
    sid = sDic['id']
    sname = sDic['name']
    path = recordsDirs + sname #f'C:/Users/g_gos/records/{sname}'
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
events_data = [{'id': event.id, 'name': event.name, 'step_id': event.step_id, 'step_name': stepIdMap[event.step_id]} for event in events]
df_events = pd.DataFrame(events_data)

# Print DataFrame
print('--Events--')
print(df_events)
print('---------')


#steps_schema_dump = steps_schema.dump(steps)
print('steps dump')
for s in steps_schema_dump:
    print(s)

events_schema_dump = events_schema.dump(events)
eventIdMap = {eDic['id']:eDic['name'] for eDic in events_schema_dump}
print('events dump')
for e in events_schema_dump:
    print(e)



#get, create and add groups



gid = 1
for eDic in events_schema_dump:
    eid = eDic['id']
    ename = eDic['name']
    sname = stepIdMap[eDic['step_id']]
    path = recordsDirs + sname + '/' + ename #f'C:/Users/g_gos/records/{sname}/{ename}'
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
group_data = [{'id': group.id, 'name': group.name, 'event_id': group.event_id, 'event_name': eventIdMap[group.event_id]} for group in groups]
df_group = pd.DataFrame(group_data)

# Print DataFrame
print('--Groups--')
print(df_group)
print('---------')

#steps_schema_dump = steps_schema.dump(steps)
print('steps dump')
for s in steps_schema_dump:
    print(s)

#events_schema_dump = events_schema.dump(events)
print('events dump')
for e in events_schema_dump:
    print(e)
    
groups_schema_dump = groups_schema.dump(groups)
print('group dump')
for g in groups_schema_dump:
    print(g)


rid = 1
for gDic in groups_schema_dump:
    gid = gDic['id']
    gname = gDic['name']
    eid = gDic['event_id']
    ename = eventIdMap[eid]
    sid = df_events[df_events['id']==eid]['step_id'].values[0]
    print('sid',sid)
    sname = stepIdMap[sid]

    path =  recordsDirs + sname + '/' + ename + '/' + gname # f'C:/Users/g_gos/records/{sname}/{ename}/{gname}'
    print(path)
    if os.path.isdir(path):
        recordList = get_sub_csvs(path)
        if len(recordList) > 0:
            print('record',recordList)
            for recordName in recordList:
                record = Record(id=rid, name=recordName.split('.')[0], group_id=gid)
                print('created',rid,recordName.split('.')[0])
                print(record)
                session.add(record)
                rid = rid+1
        else:
            verList = get_sub_dirs(path)
            for ver in verList:
                print('ver',ver)
                recordList = get_sub_csvs(path+'/'+ver)
                for recordName in recordList:
                    record = Record(id=rid, name=recordName.split('.')[0], version = ver, group_id=gid)
                    print('created',rid,recordName.split('.')[0])
                    session.add(record)
                    rid = rid+1
    else:
        print('error dir does not exist')

session.commit()

#print events table
records = session.query(Record).all()

# Convert to pandas DataFrame
record_data = [{'id': record.id, 'name': record.name, 'version':record.version, 'group_id': record.group_id} for record in records]
df_record = pd.DataFrame(record_data)

# Print DataFrame
print('--Records--')
print(df_record)
print('---------')

#steps_schema_dump = steps_schema.dump(steps)
#print('steps dump', steps_schema_dump)


aid = 1
for gDic in groups_schema_dump:
    gid = gDic['id']
    gname = gDic['name']
    eid = gDic['event_id']
    ename = eventIdMap[eid]
    sid = df_events[df_events['id']==eid]['step_id'].values[0]
    print('sid',sid)
    sname = stepIdMap[sid]

    path =  recordsDirs + sname + '/' + ename + '/' + gname # f'C:/Users/g_gos/records/{sname}/{ename}/{gname}'
    print(path)
    if os.path.isdir(path):
        agregateList = get_sub_json(path)
        if len(agregateList) > 0:
            #print('agregate',agregateList)
            for agregateName in agregateList:
                print('agregateName',agregateName)
                with open(path+'/'+agregateName) as json_file:
                    dicAgg = json.load(json_file)
                recordsList = []
                if 'records' in dicAgg:
                    recordsList = dicAgg['records']
                    print('dicAgg',recordsList,get_sub_csvs(path+'/preprocessed-VR-sessions'))
                    recordsClList = []
                    for recordName in recordsList:
                        print('recordName',recordName)
                        print('records in table ',[r.name for r in session.query(Record).filter_by(name = recordName, group_id=gid).all()])
                        record = session.query(Record).filter_by(name = recordName, group_id=gid).first()
                        print('record',record)
                        recordsClList.append(record)
                    aggregate = Aggregate(id=aid, name=agregateName, records=recordsClList, group_id=gid) #, records= recordsStr bisogna aggiungere i records
                    print('created',aid, agregateName)
                    print(aggregate)
                    session.add(aggregate)
                    session.commit()
                    aid = aid+1

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