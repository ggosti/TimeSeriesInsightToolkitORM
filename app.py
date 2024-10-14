from flask import render_template
import connexion
from db import init_db
from models import Event, RawEvent, RawGroup, RawRecord
#import views

from db import SessionLocal

# Create the application instance
app = connexion.App(__name__, specification_dir='./swagger/')
#app = config.connex_app

# Read the swagger.yml file to configure the endpoints
app.add_api('swagger.yml')

@app.route("/")
def home():
    #session = SessionLocal()
    #steps = session.query(Step).all()
    return render_template("home.html")

# get raw events,
@app.route("/raw_events")
def raw_events():
    session = SessionLocal()
    rawevents = session.query(RawEvent).all()
    return render_template("raw_events.html", rawevents=rawevents)

# get raw groups, 
@app.route("/raw_groups")
def raw_groups():
    session = SessionLocal()
    rawgroups = session.query(RawGroup).all()
    return render_template("raw_groups.html", rawgroups=rawgroups)

# get raw groups, 
@app.route("/raw_records")
def raw_records():
    session = SessionLocal()
    rawrecords = session.query(RawRecord).all()
    return render_template("raw_records.html", rawrecords=rawrecords)

# get steps
#@app.route("/steps")
#def steps():
#    session = SessionLocal()
#    steps = session.query(Step).all()
#    return render_template("steps.html", steps=steps)

# get events in step
#@app.route("/steps/<step>/events",methods=['GET'])
#def events_in_step(step):
#    session = SessionLocal()
#    print('step',step)
#    sid = views.get_step_id_by_name(session, step)
#    events = session.query(Event).filter(Event.step_id == sid).all()
#    #steps = session.query(Event).filter(event.).all()
#    return render_template("events_in_step.html", step=step, events=events)

# get events in step
@app.route("/events",methods=['GET'])
def events():
    session = SessionLocal()
    #steps = session.query(Step).all()
    events = session.query(Event).all()
    eventsNames = [e.name for e in events]
    eventsNames = list(dict.fromkeys(eventsNames))
    eventsNamesWSteps = []
    for eName in eventsNames:
        eventsSteps = [e.step for e in session.query(Event).filter(Event.name == eName).all()]
        eventsStepsNames = [es.name for es in eventsSteps]
        eventsNamesWSteps.append(eName+" "+str(eventsStepsNames))

    #steps = session.query(Event).filter(event.).all()
    return render_template("events.html", eventsNamesWSteps=eventsNamesWSteps)

# get events and show in which steps

if __name__ == '__main__':
    # Initialize the database
    init_db()
    # Run the application
    app.run(port=8081, debug=True)
