from flask import render_template
import connexion
from db import init_db
from models import Step

from db import SessionLocal

# Create the application instance
app = connexion.App(__name__, specification_dir='./swagger/')
#app = config.connex_app

# Read the swagger.yml file to configure the endpoints
app.add_api('swagger.yml')

@app.route("/")
def home():
    session = SessionLocal()
    steps = session.query(Step).all()
    return render_template("home.html", steps=steps)

if __name__ == '__main__':
    # Initialize the database
    init_db()
    # Run the application
    app.run(port=8082, debug=True)
