# TimeSeriesInsightToolkitORM
Analytics tool for time series data. Developed for csv time series data captured from 3D web applications.


# Hierarchical API with Connexion and Swagger

RESTful API using Connexion with Swagger, SQLAlchemy for ORM, and Marshmallow for serialization. 
The API manages records organized in groups, groups organized by events, and events in steps.

## Project Structure
```
my_project/
│
├── app.py
├── models.py
├── schemas.py
├── db.py
├── views.py
├── swagger/
│ └── swagger.yaml
└── requirements.txt
```

## Install dependencies

```
pip install -r requirements.txt
```

## Running the application
```sh
python app.py
```
## Access the Swagger UI:

Open your web browser and go to `http://localhost:8080/api/ui` to interact with the API using the Swagger UI.

## API Endpoints
### Steps
GET /steps: Retrieve a list of all steps.
POST /steps: Create a new step.
### Events
GET /steps/{step_id}/events: Retrieve a list of events for a specific step.
POST /steps/{step_id}/events: Create a new event for a specific step.
### Groups
GET /events/{event_id}/groups: Retrieve a list of groups for a specific event.
POST /events/{event_id}/groups: Create a new group for a specific event.
### Records
GET /groups/{group_id}/records: Retrieve a list of records for a specific group.
POST /groups/{group_id}/records: Create a new record for a specific group.
