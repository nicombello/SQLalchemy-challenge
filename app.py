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
# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station
########
session = Session(engine)
#################################################

# Flask Setup
#################################################
app = Flask(__name__)
# Flask Routes
#################################################

@app.route("/")
def Welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipition<br/>"
        f"/api/v1.0/station <br/>"
        f"/api/v1.0/tobs </br>"
        f"/api/v1.0/<start></br>"
        f"/api/v1.0/<start>/<end></br>"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    session= Session(engine)
    sel= [Measurement.date, Measurement.prcp]
    prcp_data = session.query(*sel).all()
    session.close()
 # * Convert the query results to a dictionary using `date` as the key and `prcp` as the value.

  # Return the JSON representation of your dictionary.

    precipitation = []
    for date, prcp in prcp_data:
        prcp_dict = {}
        prcp_dict["date"] = date
        prcp_dict["prcp"] = prcp
        precipitation.append(prcp_dict)

    return jsonify(precipitation)

@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)
   #Query all stations


    station_list = session.query(Station.station).\
    order_by(Station.station).all()
    
#convert tuples to normal list
    stations = list(np.ravel(station_list))

    return jsonify(stations)
    

@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)
    lateststr = session.query(Measuremnt.date).order_by(Measurement.date.desc()).first[0]
    latestdate= dt.datetime.strptime(lateststr, "%Y-%m-%d")
    querydate = dt.date(latestdate.year -1, latestdate.month, latest.day)
    sel = [Measurement.date, Measurement.tobs]
    queryresult = session.query(*sel).filter(Measurement.date>=querydate).all()

    tempertaure = list(np.ravel(queryresult))
        
    return jsonify(tempertaure)

@app.route("/api/v1.0/<start>")
def start_date(start):
    session = Session(engine)
    start_query = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
    filter(Measurement.date >=start).all()

    #tempertaure = list(np.ravel(start_query))
    start_temp = {}
    start_temp["TMIN"] = start_query[0][0]
    start_temp["TAVG"] = start_query[0][1]
    start_temp["TMAX"] = start_query[0][2]
    

    return jsonify(start_temp)

@app.route("/api/v1.0/<start>/<end>")
def start_end(start,end):
    session = Session(engine)
    start_query = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
    filter(Measurement.date >=start).filter(Measurement.date<=end).all()

    #tempertaure = list(np.ravel(start_query))
    start_temp = {}
    start_temp["TMIN"] = start_query[0][0]
    start_temp["TAVG"] = start_query[0][1]
    start_temp["TMAX"] = start_query[0][2]
    

    return jsonify(start_temp)

if __name__ =='__main__':
    app.run(debug=True)

   