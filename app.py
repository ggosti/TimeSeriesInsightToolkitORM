import connexion
from db import init_db

# Create the application instance
app = connexion.App(__name__, specification_dir='./swagger/')

# Read the swagger.yml file to configure the endpoints
app.add_api('swagger.yml')

if __name__ == '__main__':
    # Initialize the database
    init_db()
    # Run the application
    app.run(port=8080, debug=True)