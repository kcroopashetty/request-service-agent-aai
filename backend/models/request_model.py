from pydantic import BaseModel, ConfigDict
from datetime import datetime


class Request(BaseModel):
    model_config = ConfigDict(json_encoders={datetime: lambda dt: dt.isoformat()})
    request_id: str
    employee_id: str  # who raised it
    type: str  # "laptop", "mobile", "travel", "expense"
    status: str  # pending | approved | rejected | cancelled
    approver_by: str  # who approves this
