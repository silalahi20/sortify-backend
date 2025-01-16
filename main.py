from fastapi import FastAPI
from app.routes.user import router as user_router
from app.routes.learning import router as learning_router
from fastapi.middleware.cors import CORSMiddleware
from app.config.database import test_connection

app = FastAPI(title="Sortify API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.on_event("startup")
async def startup_event():
    print("Starting up...")
    await test_connection()

@app.on_event("shutdown")
async def shutdown_event():
    print("Shutting down...")

app.include_router(user_router, prefix="/users", tags=["Users"])
app.include_router(learning_router, prefix="/learning", tags=["Learning"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
