# Import Python packages, Bottle
import os, json, bottle
from bottle import run, response, static_file
from bottle import jinja2_template as template
# Import Bottle Extensions
from bottle_sqlalchemy import SQLAlchemyPlugin
# Import SQLAlchemy
from sqlalchemy import create_engine, Column, Integer, String, Text, Float
from sqlalchemy.ext.declarative import declarative_base

# Define dirs
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR, 'static')

# App Config
bottle.TEMPLATE_PATH.insert(0, os.path.join(BASE_DIR, 'templates'))
bottle.debug(True)  # Don't forget switch this to `False` on production!

# SQLite Database config
Base = declarative_base()
db_engine = create_engine('sqlite:///' + os.path.join(BASE_DIR, 'articles.db'))

# Starting App
app = bottle.default_app()

# Install Bottle plugins
app.install(SQLAlchemyPlugin(db_engine, keyword='sqlite_db'))


# Articles Database class
class CensusDB(Base):
    __tablename__ = 'CENSUS'
    id = Column(Integer, primary_key=True)
    commune = Column(Integer)
    comp_percent = Column(Float)
    comp_quantile = Column(Integer)
    cell_percent = Column(Float)
    cell_quantile = Column(Integer)
    rent_percent = Column(Float)
    rent_quantile = Column(Integer)
    imm_percent = Column(Float)
    imm_quantile = Column(Integer)
    edu_percent = Column(Float)
    edu_quantile = Column(Integer)
    own_percent = Column(Float)
    own_quantile = Column(Integer)
    uinhab_percent = Column(Float)
    uinhab_quantile = Column(Integer)
    typ = Column(String(255))


# API routes
@app.get('/api/articles/')
def get_all_articles(sqlite_db):
    """Get all Articles from Database"""
    articles = []
    articles_query = sqlite_db.query(CensusDB).all()

    for i in articles_query:
        articles.append({
            'title': i.title,
            'description': i.description
        })

    response.headers['Content-Type'] = 'application/json'
    return json.dumps({'data': articles})


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
