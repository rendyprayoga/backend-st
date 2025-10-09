from fastapi import APIRouter, HTTPException, status, Query
from typing import List, Optional
from app.crud.activity_log import (
    get_activity_logs, 
    get_top_activities, 
    get_activity_log_by_id,
    get_activity_logs_by_user,
    get_activity_logs_by_resource
)
from app.schemas.activity_log import ActivityLogResponse, TopActivityResponse

router = APIRouter(prefix="/v1/activity-logs", tags=["activity-logs"])

@router.get("/top-activities", response_model=List[TopActivityResponse])
async def read_top_activities(limit: int = Query(5, description="Number of top activities to return")):
    try:
        top_activities = await get_top_activities(limit)
        return top_activities
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving top activities: {str(e)}"
        )

@router.get("/", response_model=List[ActivityLogResponse])
async def read_activity_logs(
    skip: int = Query(0, description="Number of records to skip"),
    limit: int = Query(100, description="Number of records to return")
):
    try:
        logs = await get_activity_logs(skip, limit)
        return [
            ActivityLogResponse(
                id=str(log.id),
                action=log.action,
                resource=log.resource,
                resource_id=str(log.resource_id) if log.resource_id else None,
                user_id=str(log.user_id) if log.user_id else None,
                details=log.details,
                created_at=log.created_at
            ) for log in logs
        ]
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving activity logs: {str(e)}"
        )

@router.get("/{log_id}", response_model=ActivityLogResponse)
async def read_activity_log(log_id: str):
    log = await get_activity_log_by_id(log_id)
    if not log:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Activity log not found"
        )
    
    return ActivityLogResponse(
        id=str(log.id),
        action=log.action,
        resource=log.resource,
        resource_id=str(log.resource_id) if log.resource_id else None,
        user_id=str(log.user_id) if log.user_id else None,
        details=log.details,
        created_at=log.created_at
    )

@router.get("/user/{user_id}", response_model=List[ActivityLogResponse])
async def read_activity_logs_by_user(
    user_id: str,
    skip: int = Query(0, description="Number of records to skip"),
    limit: int = Query(100, description="Number of records to return")
):
    try:
        logs = await get_activity_logs_by_user(user_id, skip, limit)
        return [
            ActivityLogResponse(
                id=str(log.id),
                action=log.action,
                resource=log.resource,
                resource_id=str(log.resource_id) if log.resource_id else None,
                user_id=str(log.user_id) if log.user_id else None,
                details=log.details,
                created_at=log.created_at
            ) for log in logs
        ]
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving activity logs for user: {str(e)}"
        )

@router.get("/resource/{resource}/{resource_id}", response_model=List[ActivityLogResponse])
async def read_activity_logs_by_resource(
    resource: str,
    resource_id: str,
    skip: int = Query(0, description="Number of records to skip"),
    limit: int = Query(100, description="Number of records to return")
):
    try:
        logs = await get_activity_logs_by_resource(resource, resource_id, skip, limit)
        return [
            ActivityLogResponse(
                id=str(log.id),
                action=log.action,
                resource=log.resource,
                resource_id=str(log.resource_id) if log.resource_id else None,
                user_id=str(log.user_id) if log.user_id else None,
                details=log.details,
                created_at=log.created_at
            ) for log in logs
        ]
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving activity logs for resource: {str(e)}"
        )