import urllib
import os
from sqlalchemy import create_engine  
from sqlalchemy import Column, String  
from sqlalchemy.ext.declarative import declarative_base  
from sqlalchemy.orm import sessionmaker

host_server = os.environ.get("host_server", "localhost")
db_server_port = urllib.parse.quote_plus(str(os.environ.get("db_server_port", "5432")))
database_name = os.environ.get("database_name", "test")
db_email_id = urllib.parse.quote_plus(str(os.environ.get("db_email_id", "postgres")))
db_password = urllib.parse.quote_plus(str(os.environ.get("db_password", "1234")))
ssl_mode = urllib.parse.quote_plus(str(os.environ.get("ssl_mode", "prefer")))
DATABASE_URL = "postgresql://{}:{}@{}:{}/{}?sslmode={}".format(db_email_id, db_password, host_server, db_server_port, database_name, ssl_mode)
db = create_engine(DATABASE_URL)  
base = declarative_base()

class Film(base):  
    __tablename__ = 'films'

    title = Column(String, primary_key=True)
    director = Column(String)
    year = Column(String)

Session = sessionmaker(db)  
session = Session()

base.metadata.create_all(db)

# Create 
doctor_strange = Film(title="Doctor Strange", director="Scott Derrickson", year="2016")  
session.add(doctor_strange)  
session.commit()
print(type(doctor_strange))

# Read
films = session.query(Film)  
for film in films:  
    print(film.title)

# Update
# doctor_strange.title = "Some2016Film"  
# session.commit()

# Delete
# session.delete(doctor_strange)  
# session.commit()