#Step 4 - Climate App
# import dependencies 
import datetime as dt
import numpy as np
import pandas as pd
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify
from flask import request
#DataBaseSetupDataBaseSetupDataBaseSetupDataBaseSetupDataBaseSetupDataBaseSetupDataBaseSetupDataBaseSetupDataBaseSetupDataBaseSetupDataBaseSetup
# Database Setup
#DataBaseSetupDataBaseSetupDataBaseSetupDataBaseSetupDataBaseSetupDataBaseSetupDataBaseSetupDataBaseSetupDataBaseSetupDataBaseSetupDataBaseSetup

engine = create_engine("sqlite:///Resources/Hawaii.sqlite")
# reflect the database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Reflect Database into ORM class
# Save references to each table
# what tables/classes we have
for table_name in engine.table_names():
    print(table_name)
Station = Base.classes.station
Measurement = Base.classes.measurement

# Create our session (link) from Python to the DB
session = Session(engine)
# Flask Setup
#FLASKFLASKFLASKFLASKFLASKFLASKFLASKFLASKFLASKFLASKFLASKFLASKFLASK
app = Flask(__name__)
#FLASKFLASKFLASKFLASKFLASKFLASKFLASKFLASKFLASKFLASKFLASKFLASKFLASK

#ROUTESROUTESROUTESROUTESROUTESROUTESROUTESROUTESROUTESROUTESROUTESROUTES
# Flask Routes
#ROUTESROUTESROUTESROUTESROUTESROUTESROUTESROUTESROUTESROUTESROUTESROUTES
@app.route("/")
def home():
    return (
        f"<h1>API Archive</h1><p>This site is a prototype API for Precipitaion  and  Temperature readings in Hawaii.</p>"
        f"Available Routes:<br/>"
        f"to run add route string to the server url, example: 127.0.0.1:5000/api/v1.0/station<br/>"
        f"<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"- List of prior year rain totals from all stations<br/>"
        f"<br/>"
        f"- Dictionary using `date` as the key and `precipitation` as the value.<br/>"
        f"<br/>"
        f"/api/v1.0/stations<br/>"
        f"- List of Station numbers and names<br/>"
        f"<br/>"
        f"/api/v1.0/tobs<br/>"
        f"- List of prior year temperatures from all stations<br/>"
        f"<br/>"
        f"/api/v1.0/start  : example:<br/>"
        f"/http://127.0.0.1:5000/api/v1.0/2016-01-05<br/>"
        f"- When given the start date (YYYY-MM-DD), calculates the  temperatures  (`TMIN`, `TAVG`, and `TMAX`) for all dates greater than and equal to the start date<br/>"
        f"<br/>"
        f"/api/v1.0/start/end : example:<br/>"
        f"http://127.0.0.1:5000/api/v1.0/2016-01-05/2017-02-02<br/>"
        f"- When given the start and the end date (YYYY-MM-DD), calculate the calculate the `TMIN`, `TAVG`, and `TMAX` temperature for dates between the start and end date inclusive<br/>"
)
#def index():
#    return render_template("index.html")
#PRECIPITATIONPRECIPTIATIONPRECIPTIATIONPRECIPTIATIONPRECIPTIATIONPRECIPTIATIONPRECIPTIATIONPRECIPTIATIONPRECIPTIATIONPRECIPTIATION
@app.route('/api/v1.0/precipitation')
def precipitation():
    last_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    last_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    precip = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date > last_year).\
        order_by(Measurement.date).all()

# `date` and `prcp` as the keys and values
    rain_all = []
    for i in precip:
        row = {}
        row["date"] = precip[0]
        row["prcp"] = precip[1]
        rain_all.append(row)

    return jsonify(rain_all)
#PRECIPITATIONPRECIPTIATIONPRECIPTIATIONPRECIPTIATIONPRECIPTIATIONPRECIPTIATIONPRECIPTIATIONPRECIPTIATIONPRECIPTIATIONPRECIPTIATION
#STATIONSTATIONSTATIONSTATIONSTATIONSTATIONSTATIONSTATIONSTATIONSTATIONSTATIONSTATIONSTATIONSTATIONSTATIONSTATIONSTATIONSTATIONSTATION
@app.route('/api/v1.0/station')
def stations():
    sta_query = session.query(Station.name, Station.station)
    stations = pd.read_sql(sta_query.statement, sta_query.session.bind)
    print(stations)
    return jsonify(stations.to_dict())
#STATIONSTATIONSTATIONSTATIONSTATIONSTATIONSTATIONSTATIONSTATIONSTATIONSTATIONSTATIONSTATIONSTATIONSTATIONSTATIONSTATIONSTATIONSTATION
#TOBSTOBSTOBSTOBSTOBSTOBSTOBSTOBSTOBSTOBSTOBSTOBSTOBSTOBSTOBSTOBSTOBSTOBSTOBSTOBSTOBSTOBSTOBSTOBSTOBSTOBSTOBSTOBSTOBSTOBSTOBSTOBSTOBS
@app.route("/api/v1.0/tob")
def tobs():
    last_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    last_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    temperatures = session.query(Measurement.date, Measurement.tobs).\
        filter(Measurement.date > last_year).\
        order_by(Measurement.date).all()
# `date` and `tobs` as the keys and values
    temperature_all = []
    for t in temperatures:
        row = {}
        row["date"] = temperatures[0]
        row["tobs"] = temperatures[1]
        temperature_all.append(row)
    return jsonify(temperature_all)
#TOBSTOBSTOBSTOBSTOBSTOBSTOBSTOBSTOBSTOBSTOBSTOBSTOBSTOBSTOBSTOBSTOBSTOBSTOBSTOBSTOBSTOBSTOBSTOBSTOBSTOBSTOBSTOBSTOBSTOBSTOBSTOBSTOBS
#DateDateDateDateDateDateDateDateDateDateDateDateDateDateDateDateDateDateDateDateDateDateDateDateDateDateDateDateDateDateDateDateDate
@app.route("/api/v1.0/<start>")
def date1(start):

 # back one year from start date and go to the  end of data for Min/Avg/Max temp   
    start_date= dt.datetime.strptime(start, '%Y-%m-%d')
    last_year = dt.timedelta(days=365)
    start = start_date-last_year
    end =  dt.date(2017, 8, 23)
    start_data_query = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    dur = list(np.ravel(start_data_query))
    return jsonify(dur)


#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
@app.route("/api/v1.0/<start>/<end>")
def date2(start,end):

  # back one year from start/end date and get Min/Avg/Max temp     
    start_date= dt.datetime.strptime(start, '%Y-%m-%d')
    end_date= dt.datetime.strptime(end,'%Y-%m-%d')
    last_year = dt.timedelta(days=365)
    start = start_date-last_year
    end = end_date-last_year
    dur_data = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    dur = list(np.ravel(dur_data))
    return jsonify(dur)

#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

#start the server using the run() method
if __name__ == "__main__":
  app.run(debug=True, port=5000)
