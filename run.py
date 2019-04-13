# Import Python packages, Bottle
import os, json, bottle
from bottle import run, response, static_file
from bottle import jinja2_template as template
# Import Bottle Extensions
from bottle_sqlalchemy import SQLAlchemyPlugin
# Import SQLAlchemy
from sqlalchemy import create_engine, Column, Integer, String, Text, Float, Date
from sqlalchemy.ext.declarative import declarative_base

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
    id = Column("Unnamed: 0", Integer, primary_key=True)
    commune = Column("Commune", Integer)
    lon = Column("Longitude", Float)
    lat = Column("Latitude", Float)
    date = Column("Date", Date)
    us_val = Column("Value in US Dollars", Float)
    m2_val = Column("Value of m2 (US Dollars)", Float)
    m2 = Column(Float)


def remove_inst_state(a_dict):
    a_dict.pop('_sa_instance_state', None)
    return a_dict

# API routes
@app.get('/api/census/')
def get_all_census_data(sqlite_db):
    """Get all communes and their id's from Database"""
    census = []
    census_query = sqlite_db.query(CensusDB).group_by(CensusDB.commune).distinct()
    for i in census_query:
        census.append({
            'commune': i.commune
        })

    response.headers['Content-Type'] = 'application/json'
    return json.dumps({'data': census})

@app.get('/api/census/<commune>')
def get_all_commune_data(sqlite_db, commune):
    """Get all information for a particular commune"""
    commune_query = sqlite_db.query(CensusDB).filter(CensusDB.commune == commune).all()
    dat = [remove_inst_state(i.__dict__) for i in commune_query]

    print(dat)

    response.headers['Content-Type'] = 'application/json'
    return json.dumps({'data': dat})

@app.get('/api/property/<commune>')
def get_commune_property_values(sqlite_db, commune):
    """Get all properties of a particular commune"""
    commune_query = sqlite_db.query(PropertyDB).filter(PropertyDB.commune == commune).all()
    dat = [remove_inst_state(i.__dict__) for i in commune_query]

    response.headers['Content-Type'] = 'application/json'
    return json.dumps({'data':dat})

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
