from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Step, Event, Group, Record
import os

def get_sub_dirs(path):
    #print('path',path,os.listdir(path))
    subdirs = [x for x in os.listdir(path) if os.path.isdir(path+'/'+x)] #os.walk(path)]
    return subdirs

# Replace 'sqlite:///your_database.db' with your actual database connection string
DATABASE_URL = "sqlite:///data/data.db"

# Create engine
engine = create_engine(DATABASE_URL)

# Bind the engine to the metadata of the Base class so that the declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

# Create a DBSession instance
DBSession = sessionmaker(bind=engine)
session = DBSession()

# Clear existing data from tables
session.query(Step).delete()
#session.query(Event).delete()
#session.query(Group).delete()
#session.query(Record).delete()
session.commit()#

# Create steps
raw = Step(id = 1, name='raw')
proc = Step(id = 2, name='proc')

print(raw)

# Add groups to the session
session.add(raw)
session.add(proc)
session.commit()

# #get events 
# path = "C:/Users/g_gos/records/raw" #f'/var/www/html/records/raw/'
# if os.path.isdir(path): 
#     rawEvents = get_sub_dirs(path)
#     print('raw events',rawEvents)
# else:
#     print('error raw dir does not exist')


# path = "C:/Users/g_gos/records/proc" #f'/var/www/html/records/proc/'
# if os.path.isdir(path): 
#     procEvents = get_sub_dirs(path)
#     print('proc events',procEvents)
# else:
#     print('error proc dir does not exist')


# # Create and add envents to step

# for eventName in rawEvents:
#     event = Event(id=eventName)
#     session.add(event)

# for eventName in procEvents:
#     event = Event(id=eventName)
#     session.add(event)

# session.commit()

# #get groups
# rawGroups = {}
# for eventName in rawEvents:
#     path = f'C:/Users/g_gos/records/raw/{eventName}' #f'/var/www/html/records/raw/'
#     if os.path.isdir(path): 
#         rawGroups[eventName] = get_sub_dirs(path)
#         print('raw events',rawEvents)
#     else:
#         print('error raw dir does not exist')

# procGroups = {}
# for eventName in procEvents:
#     path = f'C:/Users/g_gos/records/proc/{eventName}' #f'/var/www/html/records/proc/'
#     if os.path.isdir(path): 
#         procGroups[eventName] = get_sub_dirs(path)
#         print('proc events',procEvents)
#     else:
#         print('error proc dir does not exist')

# # Create and add groups to events
# for eventName in rawEvents:
#     for groupName in rawGroups[eventName]:
#         group = Group(name=groupName, step_id=raw.id)
#         session.add(event)

# for eventName in procEvents:
#     for groupName in procGroups[eventName]:
#         group = Group(name=groupName, step_id=proc.id)
#         session.add(event)

# session.commit()

print("Database populated successfully!")