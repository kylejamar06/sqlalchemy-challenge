#  Import modules & dependencies

import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify

#  Initializing database connection, integration

engine = create_engine("sqlite:///Resources/hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)

#  Establish Table References

Measurements = Base.classes.measurement
Station = Base.classes.station

#  Create a new session, then Flask

session = Session(engine)

app = Flask(__name__)

#  Setting Flask Routes

#  Index Route Response

@app.route("/")
def welcome():
    return (
        f"Welcome! You have reached the Hawaiian Weather API Resource <br/>"
        f" <br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    # Step 1:  Use Session Method to connect Python to database
    session = Session(engine)

    # Step 2:  Session Query to pull in data for our dictionary (and subsequent JSON conversion)
    results = session.query(Measurements.date, Measurements.prcp).\
        filter(Measurements.date >= '2016-08-23').all()
    session.close()

    # Step 3:  Use Python List Comprehensions to load data into a dictionary object
    precip = []
    for date, prcp in results:
        precip_dict = {}
        precip_dict[date] = prcp
        precip.append(precip_dict)

    return jsonify(precip)

@app.route("/api/v1.0/stations")
def stations():

    session = Session(engine)

    #Query
    results = session.query(Station.station).all()
    session.close()

    #Converting list of tuples into normal list vai np.ravel method, then converting into JSON
    all_stations = list(np.ravel(results))
    return jsonify(all_stations)



if __name__ == "__main__":
    app.run(debug=True)

