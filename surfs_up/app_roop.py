# Import the dependencies.
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy import create_engine, func, inspect
from sqlalchemy.orm import Session

from flask import Flask, jsonify

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

    # Convert list of tuples into normal list
    all_stations = list(np.ravel(results))

    return jsonify(all_stations)

@app.route("/api/v1.0/tobs")
def tempobs():
    
    session = Session(engine)
    
    results = 
    








if __name__ == '__main__':
    app.run(debug=True)
