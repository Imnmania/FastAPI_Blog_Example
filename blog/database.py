from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

###################################### Sqlite DB ######################################
#######################################################################################


#================================ SET THE DATABASE URL ===============================#
SQLALCHEMY_DATABASE_URL = 'sqlite:///./blog.db'

#================================ SET THE DB ENGINE ==================================#
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}) 

#================================ CREATE A LOCAL SESSION =============================#
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

#================================ INITIALIZE THE BASE ================================#
Base = declarative_base()

