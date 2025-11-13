from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime
from typing import Optional


class Request(BaseModel):
    model_config = ConfigDict(json_encoders={datetime: lambda dt: dt.isoformat()})
    request_id: str
    employee_id: str  # who raised it
    type: str  # "laptop", "mobile", "travel", "expense"
    status: str  # pending | approved | rejected | cancelled
    approver_by: str  # who approves this
    created_at: Optional[datetime] = Field(default_factory=datetime.now)
    updated_at: Optional[datetime] = Field(default_factory=datetime.now)
