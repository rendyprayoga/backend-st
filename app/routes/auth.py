from fastapi import APIRouter, HTTPException
from app.schemas.user import UserLogin
from app.crud.user import get_user_by_email
from app.utils.auth_utils import create_access_token

router = APIRouter(
    prefix="/v1/auth",
    tags=["Auth"]
)

@router.post("/login")
async def login(data: UserLogin):
    user = await get_user_by_email(data.email)
    if not user:
        raise HTTPException(status_code=400, detail="Email tidak ditemukan")

    if user.password != data.password:
        raise HTTPException(status_code=400, detail="Password salah")


    token = create_access_token({"sub": user.email, "role": user.role})

    return {
        "message": "Login berhasil",
        "token": token,
        "user": {
            "email": user.email,
            "full_name": user.full_name,
            "role": user.role
        }
    }
