import datetime as dt
import numpy as np
import pandas as pd

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

engine = create_engine("sqlite:///hawaii.sqlite")

Base = automap_base()

Base.prepare(engine, reflect=True)

myMeasurement = Base.classes.measurement
myStation = Base.classes.station

session = Session(engine)

app = Flask(__name__)

@app.route("/")
def welcome():
    return (
        f"Hawaii Climate Analysis API<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/temp/start/end"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    
    
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    precipitation = session.query(myMeasurement.date, myMeasurement.prcp).\
        filter(myMeasurement.date >= prev_year).all()
    myPrecip = {date: precip for date, precip in precipitation}
    return jsonify(myPrecip)

@app.route("/api/v1.0/stations")
def stations():
    
    results = session.query(myStation.station).all()
    stations = list(np.ravel(results))
    return jsonify(stations=stations) 

@app.route("/api/v1.0/tobs")
def temp_monthly():
    
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    results = session.query(myMeasurement.tobs).\
        filter(myMeasurement.station == 'USC00519281').\
        filter(myMeasurement.date >= prev_year).all()

    temps = list(np.ravel(results))
    return jsonify(temps=temps) 

@app.route("/api/v1.0/temp/<start>")
@app.route("/api/v1.0/temp/<start>/<end>")
def stats(start=None, end=None):
    x = [func.min(myMeasurement.tobs), func.avg(myMeasurement.tobs), func.max(myMeasurement.tobs)]
    if not end:
        results = session.query(*x).\
            filter(myMeasurement.date >= start).all()
        temp = list(np.ravel(results))
        return jsonify(temp)
    results = session.query(*x).\
        filter(Measurement.date >= start).\
        filter(Measurement.date <= end).all()
    temp = list(np.ravel(results))
    return jsonify(temp=temp)


if __name__ == '__main__':
    app.run()
