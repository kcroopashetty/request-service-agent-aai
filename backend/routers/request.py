from fastapi import APIRouter, Depends, status
from typing import List, Optional
from models.request_model import Request
from services.request_service import RequestService
from services import request_service
from repo.request_repo import RequestRepo
from constants import DB_NAME

router = APIRouter()
repo = RequestRepo(DB_NAME)
request_service = RequestService(repo)


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_request_endpoint(request: Request):
    await request_service.create_request(request)
    return {"message": "Request added successfully"}


@router.put("/{request_id}", status_code=status.HTTP_200_OK)
async def update_request(request_id: str, request: Request):
    """Update an existing requeset record"""
    return await request_service.update_request(request_id, request)


@router.get("/", response_model=List[Request])
async def search_request_endpoint(employee_id: Optional[str] = None):
    if employee_id:
        return await request_service.get_request_by_employee_id(employee_id)
    else:
        return await request_service.get_all_requests()


@router.delete("/{request_id}")
async def delete_request_endpoint(
    request_id: str,
):
    await request_service.delete_request(request_id)
    return {"message": "Request deleted successfully"}
