from typing import List, Optional
from bson import ObjectId
from app.database import get_database
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate
from app.crud.activity_log import create_activity_log
from datetime import datetime

db = get_database()
users_collection = db["users"]

async def create_user(user: UserCreate) -> User:
    user_dict = user.dict()
    user_dict["password"] = user_dict["password"]  
    new_user = User(**user_dict)
    result = await users_collection.insert_one(new_user.dict(by_alias=True))
    
    # Log activity - FIXED: reference to 'product' changed to 'user'
    await create_activity_log(
        action="create",
        resource="user",
        resource_id=result.inserted_id,
        user_id=result.inserted_id,  
        details={"email": user.email, "full_name": user.full_name}
    )
    
    created_user = await users_collection.find_one({"_id": result.inserted_id})
    return User(**created_user)

async def get_users(skip: int = 0, limit: int = 100) -> List[User]:
    users = await users_collection.find().skip(skip).limit(limit).to_list(length=limit)
    return [User(**user) for user in users]

# async def get_user(user_id: str) -> Optional[User]:
#     if ObjectId.is_valid(user_id):
#         user = await users_collection.find_one({"_id": ObjectId(user_id)})
#         if user:
#             return User(**user)
#     return None
async def get_user(user_id: str) -> Optional[User]:
    if ObjectId.is_valid(user_id):
        doc = await users_collection.find_one({"_id": user_id})
        print(f"{doc=}")
        if doc:
            return User(**doc)   
    return None

async def get_user_by_email(email: str) -> Optional[User]:
    user = await users_collection.find_one({"email": email})
    if user:
        return User(**user)
    return None

async def update_user(user_id: str, user: UserUpdate) -> Optional[User]:
    update_data = {k: v for k, v in user.dict(exclude_unset=True).items() if v is not None}

    if update_data:
    
        update_data["updated_at"] = datetime.utcnow()

        result = await users_collection.update_one(
            {"_id": user_id},  
            {"$set": update_data}
        )

        if result.modified_count == 1:
            await create_activity_log(
                action="update",
                resource="user",
                resource_id=user_id,
                user_id=user_id,
                details=update_data
            )

            updated_user = await users_collection.find_one({"_id": user_id})
            return User(**updated_user)

    return None

async def delete_user(user_id: str) -> bool:
    if ObjectId.is_valid(user_id):
        user = await users_collection.find_one({"_id": user_id})
        
        result = await users_collection.delete_one({"_id": user_id})
        if result.deleted_count == 1:
            
            await create_activity_log(
                action="delete",
                resource="user",
                resource_id=user_id,
                user_id=user_id,  
                details={"email": user["email"], "full_name": user["full_name"]} if user else {}
            )
            return True
    return False