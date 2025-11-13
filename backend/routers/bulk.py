from fastapi import APIRouter, HTTPException
from typing import List
from models.request_model import Request
from services.request_service import RequestService
from repo.request_repo import RequestRepo
from constants import DB_NAME

router = APIRouter()
request_service = RequestService(RequestRepo(DB_NAME))


@router.post("/create")
async def bulk_create(requests: List[Request]):
    created = []
    errors = []
    
    for req in requests:
        try:
            await request_service.create_request(req)
            created.append(req.request_id)
        except Exception as e:
            errors.append({"request_id": req.request_id, "error": str(e)})
    
    return {
        "created": len(created),
        "failed": len(errors),
        "created_ids": created,
        "errors": errors
    }


@router.post("/update-status")
async def bulk_update_status(request_ids: List[str], new_status: str):
    updated = []
    errors = []
    
    for req_id in request_ids:
        try:
            requests = await request_service.get_all_requests()
            req = next((r for r in requests if r.request_id == req_id), None)
            if req:
                req.status = new_status
                await request_service.update_request(req_id, req)
                updated.append(req_id)
            else:
                errors.append({"request_id": req_id, "error": "Not found"})
        except Exception as e:
            errors.append({"request_id": req_id, "error": str(e)})
    
    return {
        "updated": len(updated),
        "failed": len(errors),
        "updated_ids": updated,
        "errors": errors
    }


@router.delete("/delete")
async def bulk_delete(request_ids: List[str]):
    deleted = []
    errors = []
    
    for req_id in request_ids:
        try:
            await request_service.delete_request(req_id)
            deleted.append(req_id)
        except Exception as e:
            errors.append({"request_id": req_id, "error": str(e)})
    
    return {
        "deleted": len(deleted),
        "failed": len(errors),
        "deleted_ids": deleted,
        "errors": errors
    }
