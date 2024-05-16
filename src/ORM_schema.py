from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base

from pydantic import BaseModel

Base = declarative_base()
# ORM schema
class Inventory(Base):
    __tablename__ = 'inventory'
    item_id = Column(String, primary_key=True)
    product_name = Column(String)
    manufacturer = Column(String)
    product_quantity = Column(Integer)

# Pydantic model
class Item(BaseModel):
    item_id: str
    product_name: str
    manufacturer: str
    product_quantity: int