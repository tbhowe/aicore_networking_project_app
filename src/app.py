from botocore.exceptions import ClientError
from fastapi import FastAPI, Request, HTTPException, Depends
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.exc import NoResultFound, IntegrityError
from sqlalchemy.orm import sessionmaker, declarative_base, Session
from sqlalchemy.orm import declarative_base
from sqlalchemy.engine.reflection import Inspector
import boto3
import logging
import json
import yaml

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

# Create AppDatabaseSession class

class AppDatabaseSession:

    def __init__(self, secret_name="db_credentials"):
        self.creds = self.load_credentials(secret_name)
        self.db_url = f"postgresql+psycopg2://{self.creds['username']}:{self.creds['password']}@{self.creds['host']}:{self.creds['port']}/{self.creds['database_name']}"
        try:
            self.engine = create_engine(self.db_url)
            print("engine created")
        except Exception as e:
            print(f' DB creation Error: {str(e)}')

        try:   
            self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
            print("session created")
        except Exception as e:
            print(f' Session creation Error: {str(e)}')

        self.Base = declarative_base()
        
       # Try to create tables
        try:
            Base.metadata.create_all(bind=self.engine)
            print("Tables created")
            inspector = Inspector.from_engine(self.engine)
            print("Available tables:", inspector.get_table_names())
        except Exception as e:
            print(f"Error creating tables: {str(e)}")

        # Load credentials from the YAML file
    @staticmethod
    def load_credentials(secret_name):
        # Create a Secrets Manager client
        session = boto3.session.Session(region_name='eu-north-1')
        client = session.client(service_name='secretsmanager')
        try:
            get_secret_value_response = client.get_secret_value(SecretId=secret_name)
        except ClientError as e:
            print(f"Unable to retrieve secret: {e}")
            return None
        else:
            secret = get_secret_value_response['SecretString']
            return json.loads(secret)

# Initialise App, DB session, logging
app = FastAPI()
session_instance = AppDatabaseSession("creds.yaml")
logging.basicConfig(filename='access.log', level=logging.INFO, format='%(asctime)s - %(message)s')

def get_db():
    db = session_instance.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Middleware for Logging
@app.middleware("http")
async def log_requests(request: Request, call_next):
    response = await call_next(request)
    log_data = {
        "client_host": request.client.host,
        "method": request.method,
        "url_path": request.url.path,
        "full_url": str(request.url),
        "user_agent": request.headers.get("user-agent"),
        "query_params": dict(request.query_params),
        "status_code": response.status_code  # Log the status code of the response
    }
    logging.info(json.dumps(log_data))
   
    return response


@app.get("/")
def read_root():
    return {"message": "How many times have I told you not to call this endpoint?"}

# FastAPI endpoints
@app.post("/api/add_new_item")
async def add_new_item(item: Item, db: Session = Depends(get_db)):
    existing_item = db.query(Inventory).filter_by(item_id=item.item_id).first()
    if existing_item:
        raise HTTPException(status_code=400, detail="Item already exists")
    new_item = Inventory(**item.dict())
    db.add(new_item)
    db.commit()
    return {"message": f"Added new item {item.product_name} with quantity {item.product_quantity}"}

@app.post("/api/update_stock_item_number")
async def update_stock_item_number(item: Item, db: Session = Depends(get_db)):
    inventory_item = db.query(Inventory).filter_by(item_id=item.item_id).one_or_none()
    if not inventory_item:
        raise HTTPException(status_code=404, detail="Item not found")
    inventory_item.product_quantity += item.product_quantity
    db.commit()
    return {"message": f"Updated stock for {item.product_name} by {item.product_quantity}"}

@app.get("/api/view_current_stock/{item_id}")
async def view_current_stock(item_id: str, db: Session = Depends(get_db)):
    inventory_item = db.query(Inventory).filter_by(item_id=item_id).one_or_none()
    if not inventory_item:
        raise HTTPException(status_code=404, detail="Item not found")
    return {
        "item_id": inventory_item.item_id,
        "product_name": inventory_item.product_name,
        "manufacturer": inventory_item.manufacturer,
        "quantity": inventory_item.product_quantity
    }

@app.delete("/api/delete_item/{item_id}")
async def delete_item(item_id: str, db: Session = Depends(get_db)):
    inventory_item = db.query(Inventory).filter_by(item_id=item_id).one_or_none()
    if not inventory_item:
        raise HTTPException(status_code=404, detail="Item not found")
    db.delete(inventory_item)
    db.commit()
    return {"message": f"Deleted item with ID {item_id}"}

@app.get("/api/view_all_items")
async def view_all_items(db: Session = Depends(get_db)):
    items = db.query(Inventory).all()
    return items

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=8000, log_level="debug")
