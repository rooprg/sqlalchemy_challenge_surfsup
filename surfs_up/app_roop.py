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
   
   one_year_date = dt.date(2017, 8, 23) - dt.timedelta(days=365)
   
   precip_subset = session.query(Measurement.date, Measurement.prcp).\
    filter(Measurement.date >= one_year_date).all()
   
   precip_table = {date: prcp for date, prcp in precip_subset}
   
   session.close()
   
   return jsonify(precip_table)

@app.route("/api/v1.0/stations")
def stations():

    session = Session(engine)

    results = session.query(Station.station).all()

    session.close()

    all_stations = list(np.ravel(results))

    return jsonify(all_stations)

@app.route("/api/v1.0/tobs")
def tempobs():
    
    session = Session(engine)
    
    one_year_date = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    
    results = session.query(Measurement.date, Measurement.tobs).\
        filter(Measurement.date >= one_year_date).\
        filter(Measurement. station == "USC00519281").all()
        
    session.close()
    
    one_station_year = list(np.ravel(results))
    
    return jsonify(one_station_year)
 
# INSTRUCTIONS:
# Return a JSON list of the minimum temperature, the average temperature, and the maximum temperature
# for a specified start.

# For a specified start, calculate Tmin, Tavg, and Tmax for all the dates greater than or equal 
# to the start date.

# A start route that:
# Accepts the start date as a parameter from the URL
# Returns the min, max, and average temperatures calculated from 
# the given start date to the end of the dataset
 
@app.route("/api/v1.0/start")
def descstatsstart():
    
    session = Session(engine)
    
    start_date = request.args.get('start_date')
    start_date = dt.datetime.strptime(start_date, '%Y-%m-%d').date()
    
    final_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    final_date = final_date[0]
    
    sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]
    
    results = session.query(*sel).\
        filter(Measurement.date.between(start_date, final_date)).all()
    
    
    desc_stats_start = []
    for result in results:
        desc_stats_start.append({
            "Min Temperature": result[0],
            "Avg Temperature": result[1],
            "Max Temperature": result[2]
        })
   
    session.close()    
        
    return jsonify(desc_stats_start)
    
if __name__ == '__main__':
    app.run(debug=True)
