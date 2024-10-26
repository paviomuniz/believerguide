# database.py
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "postgresql://believerguide:6mzIi3lN5rlOHyUX4FEgGbPNMizdDuiU@dpg-cse81rbtq21c73868b20-a.oregon-postgres.render.com/believerguide"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
