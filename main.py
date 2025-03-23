from fastapi import FastAPI
from contextlib import asynccontextmanager
from starlette.middleware import Middleware
from src.middleware.HandleExceptions import HandleExceptionsMiddleware
from fastapi.middleware.cors import CORSMiddleware
from src.routes.api import router as api_routes
import uvicorn


@asynccontextmanager
async def lifespan_context(app_instance: FastAPI):
    print("Application starting up.")
    yield
    print("Application shutting down.")


middleware = [
    Middleware(HandleExceptionsMiddleware),
    Middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])
]

app = FastAPI(lifespan=lifespan_context, middleware=middleware)




@app.get("/")
async def root():
    return {"message": "Welcome to the dummy API"}

app.include_router(api_routes, prefix="/api")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
    