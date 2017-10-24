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


####################################################
# Flask Setup
app = Flask(__name__)

####################################################
# Routes
####################################################
# Home page route
#----------------------
@app.route("/")
def home():
    return ("Hawaii Weather Data Home page!<br/>"
    "/api/v1.0/precipitation<br/>"
    "/api/v1.0/stations<br/>"
    "/api/v1.0/tobs<br/>"
    "/api/v1.0/<start><br/>"
    "/api/v1.0/<start>/<end>")

####################################################
# Precipitation route
#----------------------
 # Query for the dates and temperature observations from last year. Convert the query result to a dictionary using date as the key and tobs as the value. Return the json representation of your dictionary.
@app.route("/api/v1.0/precipitation")
def precipitation():   
     
    most_recent = session.query(Measurements.date).order_by(Measurements.date.desc()).first()
    last_date = most_recent[0]
    year_before = last_date.replace(year = (last_date.year - 1))
    year_before = year_before.strftime("%Y-%m-%d")

    precip_list = []
    precip = session.query(Stations.name, Measurements.date, Measurements.prcp).filter(Measurements.station==Stations.station).filter(Measurements.date>=year_before).order_by(Measurements.date).all()
    for p in precip:
        # print({"date":p[0],"tobs":p[1]})
        precip_list.append({"station":p[0],"date":p[1],"prcp":p[2]})

    return jsonify(precip_list)

####################################################
# Station route
#----------------------
# Return a json list of stations from the dataset.
@app.route("/api/v1.0/stations")
def stations():    
    stations = session.query(Stations.station, Stations.name, Measurements.station, func.count(Measurements.tobs)).filter(Stations.station == Measurements.station).group_by(Measurements.station).order_by(func.count(Measurements.tobs).desc()).all()
    station_List = []
    for s in stations:
        station_List.append({"station":s[0],"name":s[1]})

    return jsonify(station_List)

####################################################
# Observed temperature route
#----------------------
# Return a json list of Temperature Observations (tobs) for the previous year
@app.route("/api/v1.0/tobs")
def tobs():
    most_recent = session.query(Measurements.date).order_by(Measurements.date.desc()).first()
    last_date = most_recent[0]
    year_before = last_date.replace(year = (last_date.year - 1))
    year_before = year_before.strftime("%Y-%m-%d")

    tobs = session.query(Stations.name,Measurements.date, Measurements.tobs).filter(Measurements.station==Stations.station).filter(Measurements.date>=year_before).order_by(Measurements.date).all()
    tobs_List = []
    for t in tobs:
       tobs_List.append({"station":t[0],"date":t[1],"temperature observation":t[2]})
    
    return jsonify(tobs_List)

####################################################
 # Return a json list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.
 #----------------------
# When given the start only, calculate TMIN, TAVG, and TMAX for all dates greater than and equal to the start date.
@app.route("/api/v1.0/<start>")
def start(start_date):
   
    minimum = session.query(func.min(Measurements.tobs)).filter(Measurements.date >= start_date).scalar()
    #print(f"Minimum temp: {minimum}")
    average = session.query(func.round(func.avg(Measurements.tobs))).filter(Measurements.date >= start_date).scalar()
    # print(f"Average temp: {average}")
    maximum = session.query(func.max(Measurements.tobs)).filter(Measurements.date >= start_date).scalar()
    # print(f"Maximum temp: {maximum}")
    
    result = [{"Minimum":minimum},{"Maximum":maximum},{"Average":average}]
    
    return jsonify(result)

####################################################
# When given the start and the end date, calculate the TMIN, TAVG, and TMAX for dates between the start and end date inclusive.
@app.route("/api/v1.0/<start>/<end>")
def StartEnd(start_date,end_date):
    minimum = session.query(func.min(Measurements.tobs)).filter(Measurements.date.between(start_date, end_date)).scalar()
    # print(f"Minimum temp: {minimum}")
    average = session.query(func.round(func.avg(Measurements.tobs))).filter(Measurements.date.between(start_date, end_date)).scalar()
    # print(f"Average temp: {average}")
    maximum = session.query(func.max(Measurements.tobs)).filter(Measurements.date.between(start_date, end_date)).scalar()
    # print(f"Maximum temp: {maximum}")
    
    result = [{"Minimum":minimum},{"Maximum":maximum},{"Average":average}]
    
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)

