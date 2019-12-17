import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify

engine = create_engine('/Users/edwardkohn/Desktop/UofM-COG-DATA-PT-09-2019-U-C-master 20/Homework/10-Advanced-Data-Storage-and-Retrieval/Instructions/Resources/hawaii.sqlite')
Base = automap_base()
Base.prepare(engine,reflect=True)

Measurement = Base.classes.measurement
Station = Base.classes.station

app = Flask(__name__)

def calc_temps(start_date, end_date):
    session = Session(engine)
    """TMIN, TAVG, and TMAX for a list of dates.
    
    Args:
        start_date (string): A date string in the format %Y-%m-%d
        end_date (string): A date string in the format %Y-%m-%d
        
    Returns:
        TMIN, TAVE, and TMAX
    """
    
    return session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).all()


@app.route("/")
def homepage():
    return (
        f"/api/v1.0/precipitation:<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>" )

@app.route("/api/v1.0/stations")
def precipitation():
    session = Session(engine)
    result=session.query(Measurement.pcrp).all()
    session.close()
    
    all_precp = []
    for precp in result:
        prep_dict ={}
        prep_dict["date"] = precp
        all_precp.append(prep_dict)
    
    return jsonify(all_precp)

@app.route('/api/v1.0/stations')   
def stations():
    session=Session(engine)
    result = session.query(Station.station,Station.name)
    session.close()
    
    stations_all = []
    for station,name in result:
        station_dict = {}
        station_dict['station'] = station
        station_dict['name'] = name
        stations_all.append(station_dict)

    return jsonify(stations_all)

@app.route('/api/v1.0/tobs')
def tobs():
    session = Session(engine)
    result=session.query(Measurement.date,Measurement.tobs).filter(Measurement.date.between('2016-08-23','2017-08-23')).all()
    session.close()
    
    tob_last_year = []
    for date,tob in result:
        tob_dict = {}
        tob_dict['date'] = date
        tob_dict['tobs'] = tob
        tob_last_year.append(tob_dict)

    return jsonify(tob_last_year)

@app.route('/api/v1.0/<start>')
def start(start):

    """Return a JSON list of the minimum, average, and maximum temperatures from the start date until the end of the database."""

    session = Session(engine)
    final_date_query = session.query(func.max(func.strftime("%Y-%m-%d", Measurement.date))).all()
    session.close()
    
    max_date = final_date_query[0][0]
    temp_range = calc_temps(start, max_date)

    obs_temp_list = []
    date_dict = {'start_date': start, 'end_date': max_date}
    obs_temp_list.append(date_dict)
    obs_temp_list.append({'Observation': 'TMIN', 'Temperature': temp_range[0][0]})
    obs_temp_list.append({'Observation': 'TAVG', 'Temperature': temp_range[0][1]})
    obs_temp_list.append({'Observation': 'TMAX', 'Temperature': temp_range[0][2]})

    return jsonify(obs_temp_list)

if __name__ == '__main__':
    app.run(debug=True)








