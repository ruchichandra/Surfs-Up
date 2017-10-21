# Dependencies
from flask import Flask, jsonify
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from datetime import datetime
import datetime as dt

# Database Setup
engine = create_engine("sqlite:///hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)

# Assign the classes to respective tables
Measurements = Base.classes.measurements
Stations = Base.classes.stations

# Create session
session = Session(engine)

# Setup Flask
app = Flask(__name__)

# Home page route
@app.route("/")
def home():
    return ("Hawaii Weather Data API<br/>"
    "/api/v1.0/precipitation<br/>"
    "/api/v1.0/stations<br/>"
    "/api/v1.0/tobs<br/>"
    "/api/v1.0/start/<br/>"
    "/api/v1.0/start/end/")

if __name__ == '__main__':
    app.run(debug=True)

