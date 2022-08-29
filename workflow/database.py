from dotenv import load_dotenv
import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

load_dotenv()

host_server = os.environ.get('SERVER')
db_server_port = os.environ.get('DB_PORT')
database_name = os.environ.get('DATABASE')
db_email_id = os.environ.get('DB_EMAIL')
db_password = os.environ.get('DB_PASSWORD')
ssl_mode = os.environ.get('SSL_MODE')
DATABASE_URL = "postgresql://{}:{}@{}:{}/{}?sslmode={}".format(db_email_id, db_password, host_server, db_server_port,
                                                               database_name, ssl_mode)


engine = create_engine(
    DATABASE_URL,
    # connect_args={"check_same_thread": False},
    # pool_size=3,
    # max_overflow=0,
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
