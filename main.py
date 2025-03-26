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


CORS_ORIGINS = [
    "https://compliance.ajuniorvc.com",  # Custom domain (if you have one)
    "https://compliance-system.netlify.app",  # Default Netlify domain (update with your actual project name)
    "https://compliance-system.vercel.app",   # Default Vercel domain (update with your actual project name)
]
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_METHODS = ["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"]
CORS_ALLOW_HEADERS = [
    "Content-Type", 
    "Authorization", 
    "X-Requested-With",
    "Accept",
    "Origin",
    "Access-Control-Request-Method",
    "Access-Control-Request-Headers"
]
CORS_EXPOSE_HEADERS = [
    "Content-Length", 
    "Content-Range"
]
CORS_MAX_AGE = 600
middleware = [
    Middleware(HandleExceptionsMiddleware),
    Middleware(
        CORSMiddleware, 
        allow_origins=CORS_ORIGINS,
        allow_credentials=CORS_ALLOW_CREDENTIALS,
        allow_methods=CORS_ALLOW_METHODS,
        allow_headers=CORS_ALLOW_HEADERS,
        expose_headers=CORS_EXPOSE_HEADERS,
        max_age=CORS_MAX_AGE
    )
]

app = FastAPI(lifespan=lifespan_context, middleware=middleware)




@app.get("/")
async def root():
    return {"message": "Welcome to the dummy API"}

app.include_router(api_routes, prefix="/api")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
    