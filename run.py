# Import Python packages, Bottle
import os, json, bottle
from bottle import run, response, static_file
from bottle import jinja2_template as template
# Import Bottle Extensions
from bottle_sqlalchemy import SQLAlchemyPlugin
# Import SQLAlchemy
from sqlalchemy import create_engine, Column, Integer, String, Text, Float, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import func

from operator import itemgetter

# Define dirs
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR, 'static')

# App Config
bottle.TEMPLATE_PATH.insert(0, os.path.join(BASE_DIR, 'templates'))
bottle.debug(True)  # Don't forget switch this to `False` on production!

# SQLite Database config
Base = declarative_base()
db_engine = create_engine('sqlite:///' + os.path.join(BASE_DIR, 'data.db'))

# Starting App
app = bottle.default_app()

# Install Bottle plugins
app.install(SQLAlchemyPlugin(db_engine, keyword='sqlite_db'))


# Census Database class
class CensusDB(Base):
    __tablename__ = 'CENSUS'
    id = Column("id", Integer, primary_key=True)
    commune = Column("Commune", Integer)
    comp_percent = Column("Computer Percent", Float)
    comp_quantile = Column("Computer Quantile", Integer)
    cell_percent = Column("Cellular Percent", Float)
    cell_quantile = Column("Cellular Quantile", Integer)
    rent_percent = Column("Rent Percent", Float)
    rent_quantile = Column("Rent Quantile", Integer)
    imm_percent = Column("Immigration Percent", Float)
    imm_quantile = Column("Immigration Quantile", Integer)
    edu_percent = Column("Education Percent", Float)
    edu_quantile = Column("Education Quantile", Integer)
    own_percent = Column("Owner Percent", Float)
    own_quantile = Column("Owner Quantile", Integer)
    reg_percent = Column("Regular Percent", Float)
    reg_quantile = Column("Regular Quantile", Integer)
    uinhab_percent = Column("Uninhabited Percent", Float)
    uinhab_quantile = Column("Uninhabited Quantile", Integer)

# Property Database
class PropertyDB(Base):
    __tablename__ = 'PROPERTY'
    id = Column("index", Integer, primary_key=True)
    commune = Column("Commune", Integer)
    b_id = Column("b_id", Integer)
    lon = Column("Longitude", Float)
    lat = Column("Latitude", Float)
    date = Column("Date", Date)
    us_val = Column("Value in US Dollars", Float)
    m2_val = Column("Value of m2 (US Dollars)", Float)
    m2 = Column(Float)

# Rent Database
class RentDB(Base):
    __tablename__ = 'RENT'
    id = Column("b_id_", Integer, primary_key=True)
    max_price_lc = Column("price_aprox_local_currency_max", Float)
    avg_price_lc = Column("price_aprox_local_currency_mean", Float)
    std_price_lc = Column("price_aprox_local_currency_std", Float)
    max_price_us = Column("price_aprox_usd_max", Float)
    avg_price_us = Column("price_aprox_usd_mean", Float)
    std_price_us = Column("price_aprox_usd_std", Float)

class CommuneDB(Base):
    __tablename__ = 'COMMUNES'
    id = Column("index", Integer, primary_key=True)
    commune = Column("Commune", Integer)
    b_id = Column("b_id", Integer)

class BarrioDB(Base):
    __tablename__ = 'BARRIOS'
    id = Column("id", Integer, primary_key=True)
    name = Column("Barrio", String(255))


def remove_inst_state(a_dict):
    a_dict.pop('_sa_instance_state', None)
    return a_dict

def package_data(dat):
    response.headers['Content-Type'] = 'application/json'
    return json.dumps({'data': dat})

# API routes
@app.get('/api/barrio/')
def get_all_barrios(sqlite_db):
    """Get name and ID of all barrios"""
    query = sqlite_db.query(BarrioDB).all()
    dat = [remove_inst_state(i.__dict__) for i in query]

    response.headers['Content-Type'] = 'application/json'
    return json.dumps({'data': dat})


@app.get('/api/commune/')
def get_all_communes(sqlite_db):
    """Get all communes, their id, and the barrios in them from Database"""
    query = sqlite_db.query(CommuneDB).all()
    dic_dat = {}

    for i in query:
        if i.commune in dic_dat:
            dic_dat[i.commune].append(i.b_id)
        else:
            dic_dat[i.commune] = list()
            dic_dat[i.commune].append(i.b_id)

    dat = [{'commune':key,'barrios':value} for key,value in dic_dat.items()]

    return package_data(dat)


@app.get('/api/census/')
def get_all_census_data(sqlite_db):
    """Get all census data available"""
    query = sqlite_db.query(CensusDB).all()
    dat = [remove_inst_state(i.__dict__) for i in query]

    return package_data(dat)

@app.get('/api/rent/all/')
def get_rent_data_all_time(sqlite_db):
    """Get rent data over all time"""
    query = sqlite_db.query(RentDB).all()
    dat = [remove_inst_state(i.__dict__) for i in query]

    return package_data(dat)

@app.get('/api/rent/all/us_avg')
def get_rent_data_all_time(sqlite_db):
    """Get rent data over all time"""
    query = sqlite_db.query(RentDB.id, RentDB.avg_price_us).all()

    dat = [0] * (max(query,key=itemgetter(1))[0] + 1)
    for i in query:
        dat[i[0]] = i[1]

    return package_data(dat)


@app.get('/api/census/<commune>')
def get_all_commune_data(sqlite_db, commune):
    """Get all information for a particular commune"""
    commune_query = sqlite_db.query(CensusDB).filter(CensusDB.commune == commune).all()
    dat = [remove_inst_state(i.__dict__) for i in commune_query]

    return package_data(dat)

# TODO
# @app.get('/api/census/cell_aq')
# def get_all_commune_data(sqlite_db, commune):
#     """Get average cellular quantile for each commune"""
#     query = sqlite_db.query(CensusDB).all()
#     dat = [remove_inst_state(i.__dict__) for i in commune_query]

#     response.headers['Content-Type'] = 'application/json'
#     return json.dumps({'data': dat})

@app.get('/api/property/us_val/avg/')
def get_all_barrio_average_property_value(sqlite_db):
    """Get the average property value for each barrio in USD over all time"""
    query = sqlite_db.query(PropertyDB.b_id, func.avg(PropertyDB.us_val).label('average')).group_by(PropertyDB.b_id).all()
    print(len(query))
    dat = [0] * len(query)
    for i in query:
        dat[i[0]] = i[1]

    return package_data(dat)

# Index page route
@app.get('/')
def show_index():
    """Show Index page"""
    return template('index')


# Static files route
@app.get('/static/<filename:path>')
def get_static_files(filename):
    """Get Static files"""
    return static_file(filename, root=STATIC_DIR)


# Run server
if os.environ.get('APP_LOCATION') == 'heroku':
    run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
else:
    run(app, server='auto', host='localhost', port=8080, reloader=True, debug=True)
