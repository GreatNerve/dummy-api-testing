from fastapi import APIRouter, HTTPException, status, Depends,Form
from datetime import datetime
from pydantic import BaseModel
from src.middleware.AuthMiddleware import AuthMiddleware
from src.data.user import user_search
from src.data.task import task_data
from src.data.docoments import docoments_data
from src.data.lp import lp_data
from src.data.log import log_data

router = APIRouter()

@router.get("/")
async def root():
    return {"message": "Welcome to /api route"}

@router.post("/auth/login")
async def login(username: str = Form(...), password: str = Form(...)):
    if username == "admin@test.com" and password == "000000":
        return {
            "access_token": "valid_token",
            "token_type": "bearer"
        }
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid credentials"
    )

# Adding auth middleware for all routes below this point

@router.get("/users/me", dependencies=[Depends(AuthMiddleware())])
async def get_user_info():
    return {
        "user_id": "2f134aee-3708-4d5d-a71e-160ba0de3a01",
        "name": "Mona Bayer MD",
        "email": "Braden.Stroman@hotmail.com",
        "role": "Fund Manager",
        "mfa_enabled": False,
        "phone": ""
    }

@router.get("/users/search", dependencies=[Depends(AuthMiddleware())])
async def search_user():
    return user_search

@router.get("/tasks", dependencies=[Depends(AuthMiddleware())])
async def get_tasks(
        skip: int = 0,
        limit: int = 100
):
    tasks = task_data[skip:skip+limit]
    total = len(task_data)//limit
    return { "tasks" : tasks, "total" : total }


@router.get("/documents", dependencies=[Depends(AuthMiddleware())])
async def get_documents(
        skip: int = 0,
        limit: int = 100
):
    documents = docoments_data[skip:skip+limit]
    total = len(docoments_data)//limit
    return { "documents" : documents, "total" : total }

@router.get("/reports/tasks-stats", dependencies=[Depends(AuthMiddleware())])
async def get_tasks_stats():
    return {
        "total_tasks": 53,
        "completed_tasks": 10,
        "overdue_tasks": 10,
        "open_tasks": 10,
        "pending_tasks": 20,
        "review_required_tasks": 3
    }

@router.get("/lps", dependencies=[Depends(AuthMiddleware())])
async def get_lps(
        skip: int = 0,
        limit: int = 100
):
    lps = lp_data[skip:skip+limit]
    return lps


@router.get("/lps/search", dependencies=[Depends(AuthMiddleware())])
async def lps_search(
        name : str = None,
        skip: int = 0,
        limit: int = 100
):
    lps = [lp for lp in lp_data if name.lower() in lp["lp_name"].lower()]
    
    return lps[skip:skip+limit]


@router.get("/audit/logs", dependencies=[Depends(AuthMiddleware())])
async def audit_log(
        skip: int = 0,
        limit: int = 100
):
    logs = log_data[skip:skip+limit]
    total = len(log_data)//limit
    return { "logs" : logs, "total" : total }