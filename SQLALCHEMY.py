%matplotlib inline
from matplotlib import style
style.use('fivethirtyeight')
import matplotlib.pyplot as plt
import datetime as dt
from pandas.plotting import table


import numpy as np
import pandas as pd


import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func


engine = create_engine("sqlite:///hawaii.sqlite")

Base = automap_base()
Base.prepare(engine, reflect=True)


Base.classes.keys()


Measurement = Base.classes.measurement
Station = Base.classes.station

session = Session(engine)

prev = dt.date(2017, 8, 23) - dt.timedelta(days=365)


res = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= prev).all()


df = pd.DataFrame(res, columns=['date', 'precipitation'])
df.set_index(df['date'], inplace=True)

df = df.sort_values("date")
df = df.sort_index()

df.plot(rot=90)

df.describe()

session.query(func.count(Station.station)).all()


session.query(Measurement.station, func.count(Measurement.station)).\
    group_by(Measurement.station).order_by(func.count(Measurement.station).desc()).all()

session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).\
    filter(Measurement.station == 'USC00519281').all()


prev = dt.date(2017, 8, 23) - dt.timedelta(days=365)

res = session.query(Measurement.tobs).\
    filter(Measurement.station == 'USC00519281').\
    filter(Measurement.date >= prev).all()
df = pd.DataFrame(res, columns=['tobs'])
df.plot.hist(bins=12)
plt.tight_layout()

def calc_temps(start, end):
    """TMIN, TAVG, and TMAX for a list of dates.
    
    Args:
        start (string): A date string in the format %Y-%m-%d
        end (string): A date string in the format %Y-%m-%d
        
    Returns:
        TMIN, TAVE, and TMAX
    """
    
    return session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).filter(Measurement.date <= end).all()
print(calc_temps('2012-02-28', '2012-03-05'))


import datetime as dt

prev_start = dt.date(2018, 1, 1) - dt.timedelta(days=365)
prev_end = dt.date(2018, 1, 7) - dt.timedelta(days=365)

tmin, tavg, tmax = calc_temps(prev_start.strftime("%Y-%m-%d"), prev_end.strftime("%Y-%m-%d"))[0]
print(tmin, tavg, tmax)


fig, ax = plt.subplots(figsize=plt.figaspect(2.))
xpos = 1
yerr = tmax-tmin


bar = ax.bar(xpos, tmax, yerr=yerr, alpha=0.5, color='coral', align="center")
ax.set(xticks=range(xpos), xticklabels="a", title="Trip Avg Temp", ylabel="Temp (F)")
ax.margins(.2, .2)

fig.tight_layout()
fig.show()

start = '2012-01-01'
end = '2012-01-07'

sel = [Station.station, Station.name, Station.latitude, 
       Station.longitude, Station.elevation, func.sum(Measurement.prcp)]

res = session.query(*sel).\
    filter(Measurement.station == Station.station).\
    filter(Measurement.date >= start).\
    filter(Measurement.date <= end).\
    group_by(Station.name).order_by(func.sum(Measurement.prcp).desc()).all()
print(results)


