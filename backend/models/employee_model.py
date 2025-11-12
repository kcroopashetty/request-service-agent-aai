from pydantic import BaseModel, ConfigDict
from datetime import datetime


class Employee(BaseModel):
    model_config = ConfigDict(json_encoders={datetime: lambda dt: dt.isoformat()})
    employee_id: str
    name: str
    email: str
    department: str
