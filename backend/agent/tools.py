from services.request_service import RequestService
from services.employee_service import EmployeeService
from models.request_model import Request
from models.employee_model import Employee
from repo.request_repo import RequestRepo
from repo.employee_repo import EmployeeRepo
from constants import DB_NAME


employee_repo = EmployeeRepo(DB_NAME)
employee_service = EmployeeService(employee_repo)

request_repo = RequestRepo(DB_NAME)
request_service = RequestService(request_repo)


async def fetch_all_requests() -> dict:
    return await request_service.get_all_requests()


async def fetch_request_by_employee_id(employee_id: str) -> dict:
    return await request_service.get_request_by_employee_id(employee_id)


async def fetch_all_employees() -> dict:
    return await employee_service.get_all_employee()


async def fetch_employees_by_email(email: str) -> dict:
    return await employee_service.get_employee_by_email(email)


async def add_request(request_id: str, employee_id: str, type: str, status: str, approver_by: str) -> dict:
    """Add a new request to the database."""
    request = Request(request_id=request_id, employee_id=employee_id, type=type, status=status, approver_by=approver_by)
    return await request_service.create_request(request)


async def add_employee(employee_id: str, name: str, email: str, department: str) -> dict:
    """Add a new employee to the database."""
    employee = Employee(employee_id=employee_id, name=name, email=email, department=department)
    return await employee_service.create_employee(employee)


async def fetch_requests_by_type(type: str) -> dict:
    """Fetch all requests of a specific type (e.g., 'travel', 'laptop', 'mobile', 'expense')."""
    all_requests = await request_service.get_all_requests()
    filtered = [req for req in all_requests if req.type.lower() == type.lower()]
    return filtered


async def fetch_pending_requests() -> dict:
    """Fetch all requests with status 'pending'."""
    all_requests = await request_service.get_all_requests()
    pending = [req for req in all_requests if req.status.lower() == "pending"]
    return pending


async def update_request_status(request_id: str, new_status: str) -> dict:
    """Update the status of a specific request."""
    all_requests = await request_service.get_all_requests()
    existing = next((req for req in all_requests if req.request_id == request_id), None)
    if not existing:
        raise ValueError(f"Request {request_id} not found")
    existing.status = new_status
    return await request_service.update_request(request_id, existing)


async def delete_request(request_id: str) -> dict:
    """Delete a request from the database."""
    result = await request_service.delete_request(request_id)
    return {"success": result, "message": f"Request {request_id} deleted successfully"}


async def count_total_requests() -> dict:
    """Count the total number of requests in the database."""
    all_requests = await request_service.get_all_requests()
    return {"total_requests": len(all_requests)}


async def count_requests_by_status(status: str) -> dict:
    """Count requests by status (e.g., 'approved', 'pending', 'rejected', 'cancelled')."""
    all_requests = await request_service.get_all_requests()
    count = sum(1 for req in all_requests if req.status.lower() == status.lower())
    return {"status": status, "count": count}


async def get_department_with_most_requests() -> dict:
    """Find which department raised the most requests."""
    all_requests = await request_service.get_all_requests()
    all_employees = await employee_service.get_all_employee()
    
    emp_dept_map = {emp.employee_id: emp.department for emp in all_employees}
    dept_counts = {}
    
    for req in all_requests:
        dept = emp_dept_map.get(req.employee_id, "Unknown")
        dept_counts[dept] = dept_counts.get(dept, 0) + 1
    
    if not dept_counts:
        return {"department": None, "count": 0}
    
    max_dept = max(dept_counts, key=dept_counts.get)
    return {"department": max_dept, "count": dept_counts[max_dept], "all_departments": dept_counts}


async def get_most_recently_approved_request() -> dict:
    """Find the most recently approved request."""
    all_requests = await request_service.get_all_requests()
    approved = [req for req in all_requests if req.status.lower() == "approved" and req.updated_at]
    if not approved:
        return {"message": "No approved requests found"}
    most_recent = max(approved, key=lambda r: r.updated_at)
    return most_recent


async def get_pending_requests_older_than_days(days: int) -> dict:
    """List all requests pending for more than specified days."""
    from datetime import datetime, timedelta
    all_requests = await request_service.get_all_requests()
    cutoff_date = datetime.now() - timedelta(days=days)
    old_pending = [req for req in all_requests if req.status.lower() == "pending" and req.created_at and req.created_at < cutoff_date]
    return old_pending


async def get_approver_with_most_approvals() -> dict:
    """Find which approver approved the most requests."""
    all_requests = await request_service.get_all_requests()
    approved = [req for req in all_requests if req.status.lower() == "approved" and req.approver_by and req.approver_by.lower() != "none"]
    
    if not approved:
        return {"approver": None, "count": 0}
    
    approver_counts = {}
    for req in approved:
        approver_counts[req.approver_by] = approver_counts.get(req.approver_by, 0) + 1
    
    max_approver = max(approver_counts, key=approver_counts.get)
    return {"approver": max_approver, "count": approver_counts[max_approver], "all_approvers": approver_counts}


async def get_department_with_highest_approval_rate() -> dict:
    """Find which department has the highest approval rate."""
    all_requests = await request_service.get_all_requests()
    all_employees = await employee_service.get_all_employee()
    
    emp_dept_map = {emp.employee_id: emp.department for emp in all_employees}
    dept_stats = {}
    
    for req in all_requests:
        dept = emp_dept_map.get(req.employee_id, "Unknown")
        if dept not in dept_stats:
            dept_stats[dept] = {"total": 0, "approved": 0}
        dept_stats[dept]["total"] += 1
        if req.status.lower() == "approved":
            dept_stats[dept]["approved"] += 1
    
    for dept in dept_stats:
        dept_stats[dept]["approval_rate"] = dept_stats[dept]["approved"] / dept_stats[dept]["total"] if dept_stats[dept]["total"] > 0 else 0
    
    if not dept_stats:
        return {"department": None, "approval_rate": 0}
    
    max_dept = max(dept_stats, key=lambda d: dept_stats[d]["approval_rate"])
    return {"department": max_dept, "approval_rate": dept_stats[max_dept]["approval_rate"], "all_departments": dept_stats}


async def get_employee_with_most_rejected_requests() -> dict:
    """Find which employee has the most rejected requests."""
    all_requests = await request_service.get_all_requests()
    all_employees = await employee_service.get_all_employee()
    
    rejected_counts = {}
    for req in all_requests:
        if req.status.lower() == "rejected":
            rejected_counts[req.employee_id] = rejected_counts.get(req.employee_id, 0) + 1
    
    if not rejected_counts:
        return {"employee_id": None, "employee_name": None, "rejected_count": 0}
    
    max_emp_id = max(rejected_counts, key=rejected_counts.get)
    emp = next((e for e in all_employees if e.employee_id == max_emp_id), None)
    
    return {
        "employee_id": max_emp_id,
        "employee_name": emp.name if emp else "Unknown",
        "department": emp.department if emp else "Unknown",
        "rejected_count": rejected_counts[max_emp_id],
        "all_employees": rejected_counts
    }
