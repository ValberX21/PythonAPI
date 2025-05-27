from http.client import HTTPException
from sqlalchemy.orm import Session
from domains.Inventory.model import Inventory
from domains.Inventory.schemas import InventoryCreate, InventoryUpdate

def create_inventory(db: Session, inventory_data: InventoryCreate):
    db_inventory = Inventory(
        sneaker_id=inventory_data.sneaker_id,
        location=inventory_data.location,
        quantity=inventory_data.quantity
    )
    db.add(db_inventory)
    db.commit()
    db.refresh(db_inventory)
    return db_inventory

def get_inventory(db: Session):
    return db.query(Inventory).all()

def get_inventory_by_id(db: Session, inventory_id: int):
    inventory = db.query(Inventory).filter(Inventory.id == inventory_id).first()
    if not inventory:
        raise HTTPException(status=404, detail="Inventory not found")
    return inventory

def update_inventory(db: Session, inventory_id: int, update_data: InventoryUpdate):
    db_inventory = db.query(Inventory).filter(Inventory.id == inventory_id).first()
    
    if not db_inventory:
        raise HTTPException(status=404, detail="Inventory not found")

    if update_data.sneaker_id is not None:
        db_inventory.sneaker_id = update_data.sneaker_id
    if update_data.location is not None:
        db_inventory.location = update_data.location
    if update_data.quantity is not None:
        db_inventory.quantity = update_data.quantity

    db.commit()
    db.refresh(db_inventory)
    return db_inventory

def delete_inventory(db: Session, inventory_id: int):
    inventory = db.query(Inventory).filter(Inventory.id == inventory_id).first()

    if not inventory:
        raise HTTPException(status=404, detail="Inventory not found")

    db.delete(inventory)
    db.commit()
