# Import Bottle Extensions
from bottle_sqlalchemy import SQLAlchemyPlugin
# Import SQLAlchemy
from sqlalchemy import create_engine, Column, Integer, String, Text, Float, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import func, or_, and_

# SQLite Database config
Base = declarative_base()

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
        dat = pandas.DataFrame(dat)
        dat = dat.mean(0)
        dat = {"own": dat.loc['own'], "rent": dat.loc['rent'], "uinhab": dat.loc['uinhab']}
    else:
        dat = {"own": 0.57, "rent": 0.18, "uinhab": 0.25}

    return package_data(dat)

@app.get('/api/census/<commune>')
def get_all_commune_data(sqlite_db, commune):
    """Get all information for a particular commune"""
    commune_query = sqlite_db.query(CensusDB).filter(CensusDB.commune == commune).all()
    dat = [remove_inst_state(i.__dict__) for i in commune_query]

    return package_data(dat)
