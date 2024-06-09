# Import the dependencies.
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy import create_engine, func, inspect
from sqlalchemy.orm import Session

from flask import Flask, jsonify, request

import datetime as dt


#################################################
# Database Setup
#################################################
# Create an engine
engine = create_engine("sqlite:///hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all the available routes:"""
    return (
        f"Available Routes-<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start<br/>"
        f"/api/v1.0/start/end"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
   
   # Identify the date for one year previous
   one_year_date = dt.date(2017, 8, 23) - dt.timedelta(days=365)
   
   # Query for the specify precipitation volumes
   precip_subset = session.query(Measurement.date, Measurement.prcp).\
    filter(Measurement.date >= one_year_date).all()
   
   # Generate a dictionary using 'date' as key and 'prcp' as the value
   precip_table = {date: prcp for date, prcp in precip_subset}
   
   session.close()
   
   return jsonify(precip_table)

@app.route("/api/v1.0/stations")
def stations():

    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query for all stations
    results = session.query(Station.station).all()

    session.close()

    # Convert results into a normal list
    all_stations = list(np.ravel(results))

    return jsonify(all_stations)

@app.route("/api/v1.0/tobs")
def tempobs():
    
    # Create our session (link) from Python to the DB
    session = Session(engine)
    
    # Identify the date for one year previous
    one_year_date = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    
    # Query for a year's precipitation date for a single station
    results = session.query(Measurement.date, Measurement.tobs).\
        filter(Measurement.date >= one_year_date).\
        filter(Measurement. station == "USC00519281").all()
        
    session.close()
    
    # Convert results into a normal list
    one_station_year = list(np.ravel(results))
    
    return jsonify(one_station_year)
 

@app.route("/api/v1.0/temp/<start>")
@app.route("/api/v1.0/temp/<start>/<end>")
def temp_stats(start=None, end=None):
    
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Select the descriptive statistics to be used on observed temperature data
    sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]

    # Define the results generated if the user provides an end date (and start date)
    if end:
        results = session.query(*sel).\
            filter(Measurement.date >= start).\
            filter(Measurement.date <= end).all()
        
        # Convert results into a normal list
        tobs_start_only = list(np.ravel(results))

        return jsonify(tobs_start_only)

    # Define the results generated alternatively if only a start date is provided by the user
    else:
        results = session.query(*sel).\
            filter(Measurement.date >= start).all()
        
        # Convert results into a normal list
        tobs_other = list(np.ravel(results))

        session.close()    
        
        return jsonify(tobs_other)

if __name__ == '__main__':
    app.run(debug=True)
