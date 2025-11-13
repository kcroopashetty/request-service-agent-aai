from fastapi import APIRouter
from services.request_service import RequestService
from services.employee_service import EmployeeService
from repo.request_repo import RequestRepo
from repo.employee_repo import EmployeeRepo
from constants import DB_NAME
from collections import Counter

router = APIRouter()
request_service = RequestService(RequestRepo(DB_NAME))
employee_service = EmployeeService(EmployeeRepo(DB_NAME))


@router.get("/stats")
async def get_statistics():
    requests = await request_service.get_all_requests()
    
    status_counts = Counter(r.status for r in requests)
    type_counts = Counter(r.type for r in requests)
    
    return {
        "total": len(requests),
        "by_status": dict(status_counts),
        "by_type": dict(type_counts),
        "pending": status_counts.get("pending", 0),
        "approved": status_counts.get("approved", 0),
        "rejected": status_counts.get("rejected", 0)
    }


@router.get("/trends")
async def get_trends():
    requests = await request_service.get_all_requests()
    
    # Group by date
    from datetime import datetime
    date_counts = {}
    for r in requests:
        if hasattr(r, 'created_at') and r.created_at:
            date = r.created_at.split('T')[0]
            date_counts[date] = date_counts.get(date, 0) + 1
    
    return {"daily_requests": date_counts}


@router.get("/top-requesters")
async def get_top_requesters():
    requests = await request_service.get_all_requests()
    employees = await employee_service.get_all_employees()
    
    emp_map = {e.employee_id: e.name for e in employees}
    emp_counts = Counter(r.employee_id for r in requests)
    
    top_5 = [
        {"employee_id": emp_id, "name": emp_map.get(emp_id, "Unknown"), "count": count}
        for emp_id, count in emp_counts.most_common(5)
    ]
    
    return {"top_requesters": top_5}
