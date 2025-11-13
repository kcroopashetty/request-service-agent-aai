from typing import List
from models.approval_model import Approval
from repo.approval_repo import ApprovalRepo

class ApprovalService:
    def __init__(self, repo: ApprovalRepo):
        self.repo = repo

    async def create_approval(self, approval: Approval) -> Approval:
        await self.repo.init_db()
        await self.repo.create_approval(approval)
        return approval

    async def get_pending_approvals(self, approver_id: str) -> List[Approval]:
        await self.repo.init_db()
        return await self.repo.get_pending_approvals(approver_id)

    async def approve_request(self, approval_id: str, comments: str = None):
        await self.repo.init_db()
        await self.repo.update_approval_status(approval_id, "approved", comments)

    async def reject_request(self, approval_id: str, comments: str = None):
        await self.repo.init_db()
        await self.repo.update_approval_status(approval_id, "rejected", comments)
