from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.routes import users, products, activity_logs,auth,upload
from app.database import get_database
from app.crud.product import create_category_index
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

app = FastAPI(
    title="FastAPI V1",
    description="Crud Auth, Users, Products",
    version="1.0.0"
)
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["http://localhost:3000"], 
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",      # Untuk web frontend
        "http://127.0.0.1:3000",      # Untuk web frontend
        "http://localhost",           # Untuk Flutter web
        "http://127.0.0.1",           # Untuk Flutter web  
        "http://10.0.2.2",            #  UNTUK ANDROID EMULATOR 
        "http://10.0.2.2:8000",       #  ANDROID EMULATOR DENGAN PORT 
        "http://localhost:8000",      # Local development
        "http://127.0.0.1:8000",      # Local development
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# Include routers
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")
app.include_router(users.router)
app.include_router(products.router)
# app.include_router(orders.router)
app.include_router(activity_logs.router)
app.include_router(auth.router)
app.include_router(upload.router)

@app.on_event("startup")
async def startup_event():
    # Create indexes on startup
    await create_category_index()

# @app.get("/")
# async def root():
#     return {"message": "Welcome to FastAPI MongoDB CRUD API"}

@app.get("/v1/health")
async def health_check():
    try:
        db = get_database()
        # Test database connection
        await db.command("ping")
        return {"status": "healthy", "database": "connected"}
    except Exception as e:
        return {"status": "unhealthy", "database": "disconnected", "error": str(e)}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)