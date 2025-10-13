from fastapi import APIRouter, HTTPException, status
from typing import List
from app.crud.user import (
    create_user, get_users, get_user, update_user, delete_user, get_user_by_email
)
from app.schemas.user import UserCreate, UserUpdate, UserResponse

router = APIRouter(prefix="/api/v1/users", tags=["Users"])

@router.post(
    "/", 
    response_model=UserResponse, 
    status_code=status.HTTP_201_CREATED,
    summary="Create New User",
 
)
async def create_new_user(user: UserCreate):
    existing_user = await get_user_by_email(user.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    created_user = await create_user(user)
    return UserResponse(
        id=str(created_user.id),
        email=created_user.email,
        full_name=created_user.full_name,
        role=created_user.role,
        is_active=created_user.is_active,
        phone=created_user.phone,
        profile_picture=created_user.profile_picture,
        created_at=created_user.created_at,
        updated_at=created_user.updated_at
    )

@router.get(
    "/", 
    response_model=List[UserResponse], 
    summary="Get All Users",
   
)
async def get_all_users():
    users = await get_users()
    return [
        UserResponse(
            id=str(user.id),
            email=user.email,
            full_name=user.full_name,
            role=user.role,
            is_active=user.is_active,
            phone=user.phone,
            profile_picture=user.profile_picture,
            created_at=user.created_at,
            updated_at=user.updated_at
        ) for user in users
    ]

@router.get(
    "/{user_id}", 
    response_model=UserResponse,
    summary="Get One User",
)
async def get_single_user(user_id: str):
    user = await get_user(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return UserResponse(
        id=str(user.id),
        email=user.email,
        full_name=user.full_name,
        role=user.role, 
        is_active=user.is_active,
        phone=user.phone,
        profile_picture=user.profile_picture,
        created_at=user.created_at,
        updated_at=user.updated_at
    )

@router.put(
    "/{user_id}", 
    response_model=UserResponse,
    summary="Update Existing User",
)
async def update_existing_user(user_id: str, user: UserUpdate):
    updated_user = await update_user(user_id, user)
    if not updated_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return UserResponse(
        id=str(updated_user.id),
        email=updated_user.email,
        full_name=updated_user.full_name,
        role=updated_user.role,
        is_active=updated_user.is_active,
        phone=updated_user.phone,
        profile_picture=updated_user.profile_picture,
        created_at=updated_user.created_at,
        updated_at=updated_user.updated_at
    )

@router.delete(
    "/{user_id}", 
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete User",
)
async def delete_existing_user(user_id: str):
    success = await delete_user(user_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return None
