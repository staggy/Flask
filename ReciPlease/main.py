"""
Main file that starts the flask server.

"""
# Will import the website folder and run __init__ instantly
from website import create_app

app = create_app()

# Only if this file is ran instead of just running code
# This is for when importing these files places.
if __name__ == '__main__':
    app.run(debug=True)
    # turn Debug to False when running in production
