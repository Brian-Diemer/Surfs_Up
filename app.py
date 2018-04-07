import datetime as dt
import numpy as np
import pandas as pd

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Station = Base.classes.Station
Measurements = Base.classes.Measurements

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
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start<br/>"
        f"/api/v1.0/startend"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    measure_dict = {}
    measure_dict = session.query(Measurements.date, Measurements.tobs).all()
    return jsonify(measure_dict)


@app.route("/api/v1.0/stations")
def station_temp():
    station_dict = {}
    station_dict['station'] = session.query(Measurements.station).all()
    
    return jsonify(station_dict)


@app.route("/api/v1.0/tobs")
def temp_obs():
    temp_dict = {}
    temp_dict['tobs'] = session.query(Measurements.tobs, Measurements.date).\
        filter(Measurements.date >= (dt.date.today() - dt.timedelta(days=365))).all()
    return jsonify(temp_dict)


@app.route("/api/v1.0/start")
def recent_temp():
    start_date = '2017-04-06'
    recent_dict = {}
    recent_dict['Min'] = session.query(func.min(Measurements.tobs)).\
        filter(Measurements.date >= start_date).all()
    
    recent_dict['Max'] = session.query(func.max(Measurements.tobs)).\
        filter(Measurements.date >= start_date).all()
    
    recent_dict['Average'] = session.query(func.avg(Measurements.tobs)).\
        filter(Measurements.date >= start_date).all()
    
    return jsonify(recent_dict)


@app.route("/api/v1.0/startend")
def calc_temp():
    start_date = '2017-04-09'
    end_date = '2017-05-10'
    temp_dict = {}
    temp_dict['Min'] = session.query(func.min(Measurements.tobs)).\
        filter(Measurements.date >= start_date).\
        filter(Measurements.date <= end_date).all()
    
    temp_dict['Max'] = session.query(func.max(Measurements.tobs)).\
        filter(Measurements.date >= start_date).\
        filter(Measurements.date <= end_date).all()
    
    temp_dict['Average'] = session.query(func.avg(Measurements.tobs)).\
        filter(Measurements.date >= start_date).\
        filter(Measurements.date <= end_date).all()
    
    return jsonify(temp_dict)


if __name__ == '__main__':
    app.run(debug=True)