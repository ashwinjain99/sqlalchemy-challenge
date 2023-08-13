# Import the dependencies.
import numpy as np
import pandas as pd
import datetime as dt

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
Base.prepare(autoload_with=engine)
    
# Save references to each table
measurement = Base.classes.measurement
station = Base.classes.station

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
    return( 
           f"Welcome to the Climate API!<br/>"
           f"Available routes:<br/>"
           f"/api/v1.0/precipitation<br/>"
           f"/api/v1.0/stations<br/>"
           f"/api/v1.0/tobs<br/>"
           f"/api/v1.0/start<br/>"
           f"/api/v1.0/start/end"
    
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)
    
    # Query the date and prcp from the last year
    year_ago = dt.date(2017, 8, 23) - dt.timedelta(days = 365)
    year_data = session.query(measurement.date, measurement.prcp).filter(measurement.date >= year_ago).all()
    
    session.close()
    
    # Create dictionary of last 12 months of data, using date as the key and prcp as the value, and append values to a list
    precipitation_data = {date: prcp for date, prcp in year_data}
    
    # Return the precipitation data as a JSON response
    return jsonify(precipitation_data)


@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)
    
    # Query all the stations in the stations table and store them in a list
    station_list = [station.station for station in session.query(station.station).group_by(station.station).all()]
    
    session.close()
    
    # Return the list of station names as a JSON response
    return jsonify(station_list)


@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)
    
    # Query the date and temperature observation of the most-active station for the previous year of data.
    year_ago = dt.date(2017, 8, 23) - dt.timedelta(days = 365)
    most_active_station = session.query(measurement.date, measurement.tobs).filter(measurement.station == "USC00519281").filter(measurement.date >= year_ago).all()
    
    session.close()
    
    # Create a list of temperature observations for the previous year
    temp_tobs = [(row.date, row.tobs) for row in most_active_station]
            
    # Return the list of temperature observations as a JSON response
    return jsonify(temp_tobs)


@app.route("/api/v1.0/<start>")
def start_range(start):
    # Create our session (link) from Python to the DB
    session = Session(engine)
 
    # Conver the date string to datetime object
    start_date = dt.datetime.strptime(start, '%Y-%m-%d')
    
    # Calculate the minimum temperature, the average temperature, and the maximum temperature for all the dates greater than or equal to the start date.
    start_range_tobs = session.query(func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)).filter(measurement.date >= start_date).all()
    
    session.close()
    
    # Create a list of the min, avg, max temps after the specified start date
    start_range_list = [{"min":temp[0], "avg":temp[1], "max":temp[2]} for temp in start_range_tobs]
     
    # Return the list of temperature observations as a JSON response       
    return jsonify(start_range_list)


@app.route("/api/v1.0/<start>/<end>")
def start_end(start, end):
    # Create our session (link) from Python to the DB
    session = Session(engine)
    
    # Conver the date string to datetime object
    start_date = dt.datetime.strptime(start, '%Y-%m-%d')
    end_date = dt.datetime.strptime(end, '%Y-%m-%d')
    
    # Calculate the minimum temperature, the average temperature, and the maximum temperature for dates from the start date to the end date, inclusive
    date_range_tobs = session.query(func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs))\
                                    .filter(measurement.date >= start_date).filter(measurement.date <= end_date)
    
    session.close()
    
    # Create a list of the min, avg, max temps for dates from the start date to the end date, inclusive
    date_tobs = [{"min":min, "avg":avg, "max":max} for min, avg, max in date_range_tobs]

    # Return the list of temperature observations as a JSON response   
    return jsonify(date_tobs)


if __name__ == '__main__':
    app.run(debug=True)
    
    
