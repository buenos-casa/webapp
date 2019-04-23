# Import Python packages, Bottle
import os, json, bottle
from bottle import run, response, static_file
from bottle import jinja2_template as template
# Import Bottle Extensions
from bottle_sqlalchemy import SQLAlchemyPlugin
# Import SQLAlchemy
from sqlalchemy import create_engine, Column, Integer, String, Text, Float, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import func, or_, and_

from operator import itemgetter

from dateutil import parser as dtp

import pandas as pd

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

###################################
# Census ##########################
###################################

# Census Database class
class CensusDB(Base):
    __tablename__ = 'CENSUS'
    id = Column("id", Integer, primary_key=True)
    commune = Column("Commune", Integer)
    barrio = Column("b_id", Integer)
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

@app.get('/api/census/')
def get_all_census_data(sqlite_db):
    """Get all census data available"""
    query = sqlite_db.query(CensusDB).all()
    dat = [remove_inst_state(i.__dict__) for i in query]

    return package_data(dat)

@app.get('/api/census/commune/<commune>')
def get_all_commune_data(sqlite_db, commune):
    """Get all information for a particular commune"""
    commune_query = sqlite_db.query(CensusDB).filter(CensusDB.commune == commune).all()
    dat = [remove_inst_state(i.__dict__) for i in commune_query]

    return package_data(dat)

@app.get('/api/census/barrio/<barrio>')
def get_all_barrio_data(sqlite_db, barrio):
    """Get percentage information for a particular barrio"""
    if barrio != 'undefined':
        barrio_query = sqlite_db.query(CensusDB.own_percent, CensusDB.rent_percent, CensusDB.uinhab_percent).filter(CensusDB.barrio == barrio).all()
        dat = [{"own": i[0]/100, "rent": i[1]/100, "uinhab": i[2]/100} for i in barrio_query]
        dat = pd.DataFrame(dat)
        dat = dat.mean(0)
        dat = {"own": dat.loc['own'], "rent": dat.loc['rent'], "uinhab": dat.loc['uinhab']}
    else:
        dat = {"own": 0.57, "rent": 0.18, "uinhab": 0.08}

    return package_data(dat)

###################################
# Property Values #################
###################################

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

@app.get('/api/property/us_val/avg/')
def get_all_barrio_average_property_value(sqlite_db):
    """Get the average property value for each barrio in USD over all time"""
    query = sqlite_db.query(PropertyDB.b_id, func.avg(PropertyDB.us_val).label('average')).group_by(PropertyDB.b_id).all()
    dat = [0] * 49
    for i in query:
        dat[i[0]] = i[1]

    return package_data(dat)

###################################
# Rent ############################
###################################

# Rent Database
class RentDB(Base):
    __tablename__ = 'RENT'
    id = Column("barrio", Integer, primary_key=True)
    count = Column("count", Integer)
    usd_price = Column("mean", Float)
    tenth_percentile_count = Column("count 10th percentile", Integer)
    ninty_percentile_count = Column("count 90th percentile", Integer)
    price_min = Column("min", Float)
    price_max = Column("max", Float)
    price_std = Column("std", Float)

@app.get('/api/rent/<barrio>')
def get_barrio_summary_stats(sqlite_db, barrio):
    query = sqlite_db.query(RentDB)\
                     .filter(and_(RentDB.id == barrio))\
                     .first()
    dat = {
        'max': query.price_max,
        'avg': query.usd_price,
        'std': query.price_std
    }

    return package_data(dat)

@app.get('/api/rent/all/avg')
def get_all_barrio_of_max(sqlite_db):
    query = sqlite_db.query(RentDB.id, RentDB.usd_price).all()
    dat = [0] * 49

    for i in query:
        dat[i.id] = i.usd_price
    
    return package_data(dat)

@app.get('/api/rent/all/max')
def get_all_barrio_of_max(sqlite_db):
    query = sqlite_db.query(RentDB.id, RentDB.price_max).all()
    dat = [0] * 49

    for i in query:
        dat[i.id] = i.price_max

    return package_data(dat)

@app.get('/api/rent/all/min')
def get_all_barrio_of_min(sqlite_db):
    query = sqlite_db.query(RentDB.id, RentDB.price_min).all()
    dat = [0] * 49

    for i in query:
        dat[i.id] = i.price_min

    return package_data(dat)

@app.get('/api/rent/all/std')
def get_all_barrio_of_std(sqlite_db):
    query = sqlite_db.query(RentDB.id, RentDB.price_std).all()
    dat = [0] * 49

    for i in query:
        dat[i.id] = i.price_std

    return package_data(dat)

@app.get('/api/rent/all/tenth')
def get_all_barrio_of_tenth(sqlite_db):
    query = sqlite_db.query(RentDB.id, RentDB.tenth_percentile_count, RentDB.count).all()
    dat = [0] * 49

    for i in query:
        dat[i.id] = i.tenth_percentile_count / i.count

    return package_data(dat)

@app.get('/api/rent/all/ninty')
def get_all_barrio_of_ninty(sqlite_db):
    query = sqlite_db.query(RentDB.id, RentDB.ninty_percentile_count, RentDB.count).all()
    dat = [0] * 49

    for i in query:
        dat[i.id] = i.ninty_percentile_count / i.count

    return package_data(dat)


###################################
# Purchase Monthly ################
###################################

class PurchaseDB(Base):
    __tablename__ = 'SELL'
    id = Column("barrio", Integer, primary_key=True)
    count = Column("count", Integer)
    usd_price = Column("mean", Float)
    tenth_percentile_count = Column("count 10th percentile", Integer)
    ninty_percentile_count = Column("count 90th percentile", Integer)
    price_min = Column("min", Float)
    price_max = Column("max", Float)
    price_std = Column("std", Float)

@app.get('/api/purchase/<barrio>')
def get_barrio_summary_stats(sqlite_db, barrio):
    if(barrio != 'all'):
        query = sqlite_db.query(PurchaseDB)\
                         .filter(and_(PurchaseDB.id == barrio))\
                         .first()
        dat = {
            'max': query.price_max,
            'avg': query.usd_price,
            'std': query.price_std,
            'tenth': query.tenth_percentile_count,
            'ninty': query.ninty_percentile_count,
            'count': query.count
            }
    else:
        """Get rent data over all time"""
        query = sqlite_db.query(PurchaseDB).all()

        dat = [remove_inst_state(i.__dict__) for i in query]

    return package_data(dat)

@app.get('/api/purchase/all/avg')
def get_all_barrio_of_max(sqlite_db):
    query = sqlite_db.query(PurchaseDB.id, PurchaseDB.usd_price).all()
    dat = [0] * 49

    for i in query:
        dat[i.id] = i.usd_price

    return package_data(dat)

@app.get('/api/purchase/all/max')
def get_all_barrio_of_max(sqlite_db):
    query = sqlite_db.query(PurchaseDB.id, PurchaseDB.price_max).all()
    dat = [0] * 49

    for i in query:
        dat[i.id] = i.price_max

    return package_data(dat)

@app.get('/api/purchase/all/min')
def get_all_barrio_of_min(sqlite_db):
    query = sqlite_db.query(PurchaseDB.id, PurchaseDB.price_min).all()
    dat = [0] * 49

    for i in query:
        dat[i.id] = i.price_min

    return package_data(dat)

@app.get('/api/purchase/all/std')
def get_all_barrio_of_std(sqlite_db):
    query = sqlite_db.query(PurchaseDB.id, PurchaseDB.price_std).all()
    dat = [0] * 49

    for i in query:
        dat[i.id] = i.price_std

    return package_data(dat)

@app.get('/api/purchase/all/tenth')
def get_all_barrio_of_tenth(sqlite_db):
    query = sqlite_db.query(PurchaseDB.id, PurchaseDB.tenth_percentile_count, PurchaseDB.count).all()
    dat = [0] * 49

    for i in query:
        dat[i.id] = i.tenth_percentile_count / i.count

    return package_data(dat)

@app.get('/api/purchase/all/ninty')
def get_all_barrio_of_ninty(sqlite_db):
    query = sqlite_db.query(PurchaseDB.id, PurchaseDB.ninty_percentile_count, PurchaseDB.count).all()
    dat = [0] * 49

    for i in query:
        dat[i.id] = i.ninty_percentile_count / i.count

    return package_data(dat)

###################################
# Rent Monthly ####################
###################################

# Rent monthly
class RentMODB(Base):
    __tablename__ = 'RENT_MO'
    id = Column("index", Integer, primary_key=True)
    b_id = Column("barrio", Integer)
    count = Column("count", Integer)
    usd_price = Column("mean", Float)
    tenth_percentile_count = Column("count 10th percentile", Integer)
    ninty_percentile_count = Column("count 90th percentile", Integer)
    price_min = Column("min", Float)
    price_max = Column("max", Float)
    price_std = Column("std", Float)
    date = Column("date", Date)

# Barrio rental price average monthly
@app.get('/api/rent/monthly/<barrio>')
def get_monthly_rent(sqlite_db, barrio):
    query = sqlite_db.query(RentMODB.b_id, BarrioDB.name, RentMODB.date, RentMODB.usd_price).filter(RentMODB.b_id == barrio).join(BarrioDB, BarrioDB.id == RentMODB.b_id).all()
    dat = [{'group': i.name.title(), 'key': datetime_encoding(str(i.date)), 'value': i.usd_price} for i in query]

    return package_data(dat)

###################################
# Sell Monthly ####################
###################################

# Selling monthly
class SellMODB(Base):
    __tablename__ = 'SELL_MO'
    id = Column("index", Integer, primary_key=True)
    b_id = Column("barrio", Integer)
    count = Column("count", Integer)
    usd_price = Column("mean", Float)
    tenth_percentile_count = Column("count 10th percentile", Integer)
    ninty_percentile_count = Column("count 90th percentile", Integer)
    price_min = Column("min", Float)
    price_max = Column("max", Float)
    price_std = Column("std", Float)
    date = Column("date", Date)

# Barrio rental price average monthly
@app.get('/api/purchase/monthly/<barrio>')
def get_monthly_purchase(sqlite_db, barrio):
    query = sqlite_db.query(SellMODB.id, BarrioDB.name, SellMODB.date, SellMODB.usd_price).join(BarrioDB, BarrioDB.id == SellMODB.b_id).filter(and_(SellMODB.b_id == barrio)).all()
    dat = [{'group': i.name.title(), 'key': datetime_encoding(str(i.date)), 'value': i.usd_price} for i in query]

    return package_data(dat)

# Get property sales data per month for all of the years for all barrios
@app.get('/api/purchase/monthly/all')
def get_all_monthly_sell(sqlite_db):
    '''
    Return Object:

    b_id: Barrio ID
    barrio: Barrio Name
    Month: Month and year in the format mm/yyyy
    Mean Price for the Month
    '''
    query = sqlite_db.query(SellMODB.id, BarrioDB.name, SellMODB.date, SellMODB.usd_price, SellMODB.local_price).join(BarrioDB, BarrioDB.id == SellMODB.b_id).all()
    dat = [{'group': i.name.title(), 'key': datetime_encoding(str(i.date)), 'value': i.usd_price} for i in query]
       
    return package_data(dat)

###################################
# Sports DB #######################
###################################

class SportsDB(Base):
    __tablename__ = 'SPORT'
    id = Column("index", Integer, primary_key=True)
    name = Column("Name", String(255))
    lon = Column("Longitude", Float)
    lat = Column("Latitude", Float)
    kind = Column("Type", String(255))
    b_id = Column(Integer)

@app.get('/api/sports/all')
def get_all_sports_data(sqlite_db):
    """"""
    query = sqlite_db.query(SportsDB.b_id, func.count(SportsDB.id).label('per_barrio')).group_by(SportsDB.b_id).all()
    dat = [0] * 49 #number of barrios
    for i in query:
        dat[i[0]] = i[1]

    return package_data(dat)

###################################
# Health DB #######################
###################################

class HealthDB(Base):
    __tablename__ = 'HEALTH'
    id = Column("index", Integer, primary_key=True)
    name = Column("Name", String(255))
    lon = Column("Longitude", Float)
    lat = Column("Latitude", Float)
    kind = Column("Type", String(255))
    b_id = Column(Integer)

@app.get('/api/health/all')
def get_all_health_data(sqlite_db):
    """"""
    query = sqlite_db.query(HealthDB.b_id, func.count(HealthDB.id).label('per_barrio')).group_by(HealthDB.b_id).all()
    dat = [0] * 49 #number of barrios
    for i in query:
        dat[i[0]] = i[1]

    return package_data(dat)

@app.get('/api/health/hospital/count')
def get_hospitals_per_barrio(sqlite_db):
    """"""
    query = sqlite_db.query(HealthDB.b_id, func.count(HealthDB.id).label('per_barrio'))\
                     .filter(HealthDB.kind.contains('hospital'))\
                     .group_by(HealthDB.b_id).all()
    dat = [0] * 49 #number of barrios
    for i in query:
        dat[i[0]] = i[1]

    return package_data(dat)

###################################
# Culture DB ######################
###################################

class CultureDB(Base):
    __tablename__ = 'CULTURE'
    id = Column("index", Integer, primary_key=True)
    name = Column("Name", String(255))
    lon = Column("Longitude", Float)
    lat = Column("Latitude", Float)
    kind = Column("Type", String(255))
    b_id = Column(Integer)

@app.get('/api/culture/all')
def get_all_culture_data(sqlite_db):
    """"""
    query = sqlite_db.query(CultureDB.b_id, func.count(CultureDB.id).label('per_barrio')).group_by(CultureDB.b_id).all()
    dat = [0] * 49 #number of barrios
    for i in query:
        dat[i[0]] = i[1]

    return package_data(dat)

###################################
# Humanity DB #####################
###################################

class HumanityDB(Base):
    __tablename__ = 'HUMANITY'
    id = Column("index", Integer, primary_key=True)
    name = Column("Name", String(255))
    lon = Column("Longitude", Float)
    lat = Column("Latitude", Float)
    kind = Column("Type", String(255))
    b_id = Column(Integer)

@app.get('/api/humanity/elderly_care/count')
def get_elderly_care_per_barrio(sqlite_db):
    """"""
    query = sqlite_db.query(HumanityDB.b_id, func.count(HumanityDB.id).label('per_barrio'))\
                     .filter(or_(HumanityDB.kind.contains('retire'),HumanityDB.kind.contains('elder')))\
                     .group_by(HumanityDB.b_id).all()
    dat = [0] * 49 #number of barrios
    for i in query:
        dat[i[0]] = i[1]

    return package_data(dat)

@app.get('/api/humanity/elderly_care')
def get_elderly_care(sqlite_db):
    """"""
    query = sqlite_db.query(HumanityDB).filter(or_(HumanityDB.kind.contains('retire'),HumanityDB.kind.contains('elder')))\
                     .all()
    q_dat = [remove_inst_state(i.__dict__) for i in query]
    dat = [None] * 49 #number of barrios
    for i, row in enumerate(q_dat):
        if(dat[row['b_id']] == None):
            dat[row['b_id']] = list()
        row['name'] = row['name'].title()
        dat[row['b_id']].append(row)

    return package_data(dat)

@app.get('/api/humanity/all')
def get_all_humanity_data(sqlite_db):
    """"""
    query = sqlite_db.query(HumanityDB.b_id, func.count(HumanityDB.id).label('per_barrio')).group_by(HumanityDB.b_id).all()
    dat = [0] * 49 #number of barrios
    for i in query:
        dat[i[0]] = i[1]

    return package_data(dat)

###################################
# Commune DB ######################
###################################

class CommuneDB(Base):
    __tablename__ = 'COMMUNES'
    id = Column("index", Integer, primary_key=True)
    commune = Column("Commune", Integer)
    b_id = Column("b_id", Integer)

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

###################################
# Barrio DB #######################
###################################

class BarrioDB(Base):
    __tablename__ = 'BARRIOS'
    id = Column("id", Integer, primary_key=True)
    name = Column("Barrio", String(255))
    text = Column("Text", String)

@app.get('/api/barrio/')
def get_all_barrios(sqlite_db):
    """Get name and ID of all barrios"""
    query = sqlite_db.query(BarrioDB).order_by(BarrioDB.id).all()
    dat = [remove_inst_state(i.__dict__) for i in query]

    for i in dat:
        i['name'] = i['name'].title()

    response.headers['Content-Type'] = 'application/json'
    return json.dumps({'data': dat})

###################################
# Feature Importance DB ###########
###################################


class ImportanceDB(Base):
    __tablename__ = 'IMPORTANCE'
    id = Column("id", Integer, primary_key=True)
    feature = Column(String(255))
    score = Column(Float)
    year = Column(Integer)
    b_id = Column(Integer)

@app.get('/api/importance/<year>/<barrio>')
def get_importance(sqlite_db, year, barrio):
    """Get feature importance in order of importance for a barrio or all if 'all' passed in"""
    dat = []
    if barrio == 'all':
        # TODO
        pass
    else:
        query = sqlite_db.query(ImportanceDB).filter(and_(ImportanceDB.year == year, ImportanceDB.b_id == barrio)).all()
        dat = [{'key': i.feature, 'value': i.score} for i in query]
        dat = sorted(dat, key=lambda k: k['key'])

    return package_data(dat)


###################################
# Mislabelled Importance DB #######
###################################

class MislabelledDB(Base):
    __tablename__ = 'MISLABELLED'
    id = Column("Unnamed: 0", Integer, primary_key=True)
    date = Column("created_on", String(255))
    kind = Column("property_type", String(255))
    lat = Column(Float)
    lon = Column(Float)
    price = Column("price usd", Float)
    b_id = Column(Integer)
    c_b_id = Column(Integer)

@app.get('/api/misclassified/<barrio>/points')
def get_misclass_points(sqlite_db, barrio):
    query = sqlite_db.query(MislabelledDB).filter(MislabelledDB.b_id == barrio).all()
    dat = [{'lon': i.lon,
            'lat': i.lat,
            'hue': i.price,
            'data': {'misclass_as': i.c_b_id, 'kind': i.kind, 'date': datetime_encoding(i.date)},
            } for i in query]

    return package_data(dat)

###################################
# Packaging Functions##############
###################################

def remove_inst_state(a_dict):
    a_dict.pop('_sa_instance_state', None)
    return a_dict

def package_data(dat):
    response.headers['Content-Type'] = 'application/json'
    return json.dumps({'data': dat})

def datetime_encoding(date_str):
    return dtp.parse(date_str).isoformat()


###################################
# Normal Routes (DO NOT CHANGE)####
###################################
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
