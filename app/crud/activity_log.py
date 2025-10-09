from typing import List, Optional
from bson import ObjectId
from app.database import get_database
from app.models.activity_log import ActivityLog
from app.schemas.activity_log import ActivityLogCreate

db = get_database()
activity_logs_collection = db["activity_logs"]

async def create_activity_log(
    action: str,
    resource: str,
    resource_id: Optional[ObjectId] = None,
    user_id: Optional[ObjectId] = None,
    details: Optional[dict] = None
):
    log_data = {
        "action": action,
        "resource": resource,
        "resource_id": resource_id,
        "user_id": user_id,
        "details": details
    }
    new_log = ActivityLog(**log_data)
    result = await activity_logs_collection.insert_one(new_log.dict(by_alias=True))
    return result.inserted_id

async def get_activity_logs(skip: int = 0, limit: int = 100) -> List[ActivityLog]:
    logs = await activity_logs_collection.find().sort("created_at", -1).skip(skip).limit(limit).to_list(length=limit)
    return [ActivityLog(**log) for log in logs]

async def get_activity_log_by_id(log_id: str) -> Optional[ActivityLog]:
    if ObjectId.is_valid(log_id):
        log = await activity_logs_collection.find_one({"_id": ObjectId(log_id)})
        if log:
            return ActivityLog(**log)
    return None

async def get_top_activities(limit: int = 5) -> List[dict]:
    pipeline = [
        {
            "$group": {
                "_id": "$action",
                "count": {"$sum": 1}
            }
        },
        {"$sort": {"count": -1}},
        {"$limit": limit},
        {
            "$project": {
                "action": "$_id",
                "count": 1,
                "_id": 0
            }
        }
    ]
    
    result = await activity_logs_collection.aggregate(pipeline).to_list(length=limit)
    return result

async def get_activity_logs_by_user(user_id: str, skip: int = 0, limit: int = 100) -> List[ActivityLog]:
    if ObjectId.is_valid(user_id):
        logs = await activity_logs_collection.find(
            {"user_id": ObjectId(user_id)}
        ).sort("created_at", -1).skip(skip).limit(limit).to_list(length=limit)
        return [ActivityLog(**log) for log in logs]
    return []

async def get_activity_logs_by_resource(resource: str, resource_id: str, skip: int = 0, limit: int = 100) -> List[ActivityLog]:
    if ObjectId.is_valid(resource_id):
        logs = await activity_logs_collection.find(
            {"resource": resource, "resource_id": ObjectId(resource_id)}
        ).sort("created_at", -1).skip(skip).limit(limit).to_list(length=limit)
        return [ActivityLog(**log) for log in logs]
    return []