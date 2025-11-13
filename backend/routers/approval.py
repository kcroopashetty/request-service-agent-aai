from fastapi import APIRouter
from typing import List
from models.approval_model import Approval
from services.approval_service import ApprovalService
from repo.approval_repo import ApprovalRepo
from constants import DB_NAME

router = APIRouter()
approval_service = ApprovalService(ApprovalRepo(DB_NAME))

@router.post("/")
async def create_approval(approval: Approval):
    await approval_service.create_approval(approval)
    return {"message": "Approval created successfully"}

@router.get("/pending/{approver_id}", response_model=List[Approval])
async def get_pending_approvals(approver_id: str):
    return await approval_service.get_pending_approvals(approver_id)

@router.post("/{approval_id}/approve")
async def approve(approval_id: str, comments: str = None):
    await approval_service.approve_request(approval_id, comments)
    return {"message": "Request approved"}

@router.post("/{approval_id}/reject")
async def reject(approval_id: str, comments: str = None):
    await approval_service.reject_request(approval_id, comments)
    return {"message": "Request rejected"}
