from fastapi import FastAPI
from app.routes.user import router as user_router
from app.routes.progress import router as progress_router
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


@app.get("/")
async def root():
    return {"message": "Welcome to SORTIFY : Basic Sorting Virtual Lab"}


app.include_router(user_router, prefix="/users", tags=["Users"])
app.include_router(progress_router, prefix="/progress", tags=["Progress"])


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
