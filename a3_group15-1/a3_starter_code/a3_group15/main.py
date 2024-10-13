from website import create_app
from website.models import init_db

# Creates our app
app = create_app()  

# Activate the database
init_db(app)

# Launch the app
if __name__ == "__main__":
    app.run(debug=True)
