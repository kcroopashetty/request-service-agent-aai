from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class Approval(BaseModel):
    approval_id: str
    request_id: str
    approver_id: str
    approval_level: int  # 1, 2, 3
    status: str  # pending, approved, rejected
    comments: Optional[str] = None
    approved_at: Optional[str] = None
    created_at: str = datetime.utcnow().isoformat()
