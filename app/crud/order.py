from typing import List, Optional
from bson import ObjectId
from app.database import get_database
from app.models.order import Order
from app.schemas.order import OrderCreate, OrderUpdate
from app.crud.activity_log import create_activity_log

db = get_database()
orders_collection = db["orders"]

async def create_order(order: OrderCreate) -> Order:
    order_dict = order.dict()
    # Convert string IDs to ObjectId
    order_dict["user_id"] = ObjectId(order_dict["user_id"])
    for item in order_dict["items"]:
        item["product_id"] = ObjectId(item["product_id"])
    
    new_order = Order(**order_dict)
    result = await orders_collection.insert_one(new_order.dict(by_alias=True))
    
    # Log activity - FIXED: Added user_id parameter
    await create_activity_log(
        action="create",
        resource="order",
        resource_id=result.inserted_id,
        user_id=order_dict["user_id"],  # User who created the order
        details={
            "total_amount": order.total_amount,
            "item_count": len(order.items),
            "status": "pending"
        }
    )
    
    created_order = await orders_collection.find_one({"_id": result.inserted_id})
    return Order(**created_order)

async def get_orders(skip: int = 0, limit: int = 100, user_id: Optional[str] = None) -> List[Order]:
    query = {}
    if user_id and ObjectId.is_valid(user_id):
        query["user_id"] = ObjectId(user_id)
    
    orders = await orders_collection.find(query).skip(skip).limit(limit).to_list(length=limit)
    return [Order(**order) for order in orders]

async def get_order(order_id: str) -> Optional[Order]:
    if ObjectId.is_valid(order_id):
        order = await orders_collection.find_one({"_id": ObjectId(order_id)})
        if order:
            return Order(**order)
    return None

async def update_order(order_id: str, order: OrderUpdate) -> Optional[Order]:
    if ObjectId.is_valid(order_id):
        # Get current order first to get user_id for logging
        current_order = await orders_collection.find_one({"_id": ObjectId(order_id)})
        
        update_data = {k: v for k, v in order.dict(exclude_unset=True).items() if v is not None}
        if update_data:
            update_data["updated_at"] = Order().updated_at
            result = await orders_collection.update_one(
                {"_id": ObjectId(order_id)}, {"$set": update_data}
            )
            if result.modified_count == 1:
                # Log activity - FIXED: Correct parameters and action
                await create_activity_log(
                    action="update",
                    resource="order",
                    resource_id=ObjectId(order_id),
                    user_id=current_order["user_id"] if current_order else None,
                    details=update_data
                )
                
                updated_order = await orders_collection.find_one({"_id": ObjectId(order_id)})
                return Order(**updated_order)
    return None

async def delete_order(order_id: str) -> bool:
    if ObjectId.is_valid(order_id):
        # Get order first to get user_id for logging
        order = await orders_collection.find_one({"_id": ObjectId(order_id)})
        
        result = await orders_collection.delete_one({"_id": ObjectId(order_id)})
        if result.deleted_count == 1:
            # Log activity - FIXED: Added user_id parameter
            await create_activity_log(
                action="delete",
                resource="order",
                resource_id=ObjectId(order_id),
                user_id=order["user_id"] if order else None,
                details={
                    "total_amount": order["total_amount"] if order else 0,
                    "status": order["status"] if order else "unknown"
                }
            )
            return True
    return False