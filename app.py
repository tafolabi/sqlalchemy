import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

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
    """List all available api routes."""
    return (
        f"/api/precipitation <br/>" 
        f"/api/stations <br/>"
        f"/api/temperature <br/>"
        f"/api/<start>"
       
    )


@app.route("/api/precipitation")
def precipitation():
    """Return a list of all passenger names"""
    # Query for precipitation
    query = session.query(Measurement.date,Measurement.prcp).filter(Measurement.date>'2016-08-22').order_by(Measurement.date).all()

    # Create a dictionary from the row data and append to a list of all_passengers
    precipitation = []
    for date, prcp in query:
        precipitation_dict = {}
        precipitation_dict ["date"] = date
        precipitation_dict ["prcp"] = prcp
        precipitation.append(precipitation_dict)
        

    return jsonify(precipitation)

    

@app.route("/api/stations")
def station():
    """Return a list of all passenger names"""
    # Query for station
    station_freq = session.query(Measurement.station,func.count(Measurement.station)).\
        group_by(Measurement.station).order_by(func.count(Measurement.station).desc()).all()



     # Convert list of tuples into normal list
    station_list= list(np.ravel(station_freq ))

    return jsonify(station_list)


@app.route("/api/temperature")
def temperature():
    
    # Query for temperature
    query_station = session.query(Measurement.date,Measurement.tobs).filter(Measurement.date>'2016-08-17',Measurement.station=='USC00519281').\
    order_by(Measurement.date).all()
    tobs_list= list(np.ravel(query_station))
    
    return jsonify(tobs_list)


@app.route("/api/<start>")
def calc_temps(start_date):
    """TMIN, TAVG, and TMAX for a list of dates."""
    result_start=session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
    filter(func.strftime("%m-%d", Measurement.date) >= start_date)
        
   
    table = []
    for r in result_start:
       table_dict= {}
       table_dict["start date"] = start_date
       table_dict["end date"] = end_date
       table_dict["TAVE"] = float(r[0])
       table_dict["TMAX"] = float(r[1])
       table_dict["TMIN"] = float(r[2])
       table.append(table_dict)
        
        
    return jsonify(table_dict)
    

@app.route("/api/<start>")
def calc_temps(start_date):
    """TMIN, TAVG, and TMAX for a list of dates."""
    result_start=session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
    filter(func.strftime("%m-%d", Measurement.date) >= start_date)
        
   
    table = []
    for r in result_start:
       table_dict= {}
       table_dict["start date"] = start_date
       table_dict["end date"] = end_date
       table_dict["TAVE"] = float(r[0])
       table_dict["TMAX"] = float(r[1])
       table_dict["TMIN"] = float(r[2])
       table.append(table_dict)
        
        
    return jsonify(table_dict)   
    #return session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        #filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).all()


if __name__ == '__main__':
    app.run(debug=True)