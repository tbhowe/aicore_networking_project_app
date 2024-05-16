from ORM_schema import Inventory
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.exc import NoResultFound, IntegrityError
from sqlalchemy.orm import sessionmaker, declarative_base, Session
from sqlalchemy.orm import declarative_base
import logging
import json
import yaml

class AppDatabaseSession:

    def __init__(self, credsfile='creds.yaml'):
        self.creds = self.load_credentials(credsfile)
        self.db_url = f"postgresql+psycopg2://{self.creds['username']}:{self.creds['password']}@{self.creds['host']}:{self.creds['port']}/{self.creds['database_name']}"
        self.engine = create_engine(self.db_url)
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        self.Base = declarative_base()
        self.Base.metadata.create_all(bind=self.engine)

        # Load credentials from the YAML file
    @staticmethod
    def load_credentials(filepath='creds.yaml'):
        with open(filepath, 'r') as file:
            data = yaml.safe_load(file)
        return data
    
    Base = declarative_base()
    
    class Inventory(Base):
        __tablename__ = 'inventory'
        item_id = Column(String, primary_key=True)
        product_name = Column(String)
        manufacturer = Column(String)
        product_quantity = Column(Integer)


if __name__ == '__main__':
    db = AppDatabaseSession()
    print(db.creds)
    print(db.db_url)
    print(db.engine)
    print(db.SessionLocal)
    print(db.Base)
    print(db.Inventory)