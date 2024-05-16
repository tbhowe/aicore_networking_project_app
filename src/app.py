
from dbsession import AppDatabaseSession
from ORM_schema import Item, Inventory
from fastapi import FastAPI, Request, HTTPException, Depends
from sqlalchemy.orm import sessionmaker, declarative_base, Session
import logging
import json

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

@app.get("/api/view_current_stock/{product_name}")
async def view_current_stock(product_name: str, db: Session = Depends(get_db)):
    inventory_item = db.query(Inventory).filter_by(product_name=product_name).one_or_none()
    if not inventory_item:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"product_name": inventory_item.product_name, "quantity": inventory_item.product_quantity}

@app.delete("/api/delete_item/{product_name}")
async def delete_item(product_name: str, db: Session = Depends(get_db)):
    inventory_item = db.query(Inventory).filter_by(product_name=product_name).one_or_none()
    if not inventory_item:
        raise HTTPException(status_code=404, detail="Item not found")
    db.delete(inventory_item)
    db.commit()
    return {"message": f"Deleted item {product_name}"}

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=80, log_level="debug")

