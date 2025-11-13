"""
Advanced AI Agent Tools - Enhanced Analytics & Insights
"""
from services.request_service import RequestService
from services.employee_service import EmployeeService
from repo.request_repo import RequestRepo
from repo.employee_repo import EmployeeRepo
from constants import DB_NAME
from datetime import datetime, timedelta
from collections import defaultdict

employee_repo = EmployeeRepo(DB_NAME)
employee_service = EmployeeService(employee_repo)
request_repo = RequestRepo(DB_NAME)
request_service = RequestService(request_repo)


async def get_request_trends_by_month() -> dict:
    """Analyze request trends by month for the last 6 months."""
    all_requests = await request_service.get_all_requests()
    monthly_counts = defaultdict(int)
    
    for req in all_requests:
        if hasattr(req, 'created_at') and req.created_at:
            month_key = req.created_at.strftime("%Y-%m")
            monthly_counts[month_key] += 1
    
    return {"monthly_trends": dict(sorted(monthly_counts.items()))}


async def get_employee_request_summary(employee_id: str) -> dict:
    """Get comprehensive summary of an employee's requests."""
    all_requests = await request_service.get_all_requests()
    all_employees = await employee_service.get_all_employee()
    
    emp = next((e for e in all_employees if e.employee_id == employee_id), None)
    if not emp:
        return {"error": f"Employee {employee_id} not found"}
    
    emp_requests = [r for r in all_requests if r.employee_id == employee_id]
    
    status_breakdown = defaultdict(int)
    type_breakdown = defaultdict(int)
    
    for req in emp_requests:
        status_breakdown[req.status] += 1
        type_breakdown[req.type] += 1
    
    return {
        "employee_id": employee_id,
        "employee_name": emp.name,
        "department": emp.department,
        "total_requests": len(emp_requests),
        "status_breakdown": dict(status_breakdown),
        "type_breakdown": dict(type_breakdown),
        "approval_rate": status_breakdown["approved"] / len(emp_requests) if emp_requests else 0
    }


async def get_approval_time_statistics() -> dict:
    """Calculate average time taken for request approvals."""
    all_requests = await request_service.get_all_requests()
    approved = [r for r in all_requests if r.status.lower() == "approved" and hasattr(r, 'created_at') and hasattr(r, 'updated_at')]
    
    if not approved:
        return {"message": "No approved requests with timestamps"}
    
    total_time = sum((r.updated_at - r.created_at).total_seconds() for r in approved)
    avg_time_seconds = total_time / len(approved)
    avg_time_days = avg_time_seconds / 86400
    
    return {
        "total_approved": len(approved),
        "average_approval_time_days": round(avg_time_days, 2),
        "average_approval_time_hours": round(avg_time_seconds / 3600, 2)
    }


async def get_request_type_popularity() -> dict:
    """Rank request types by popularity."""
    all_requests = await request_service.get_all_requests()
    type_counts = defaultdict(int)
    
    for req in all_requests:
        type_counts[req.type] += 1
    
    sorted_types = sorted(type_counts.items(), key=lambda x: x[1], reverse=True)
    
    return {
        "most_popular": sorted_types[0] if sorted_types else None,
        "rankings": [{"type": t, "count": c} for t, c in sorted_types]
    }


async def get_department_comparison() -> dict:
    """Compare all departments across multiple metrics."""
    all_requests = await request_service.get_all_requests()
    all_employees = await employee_service.get_all_employee()
    
    emp_dept_map = {emp.employee_id: emp.department for emp in all_employees}
    dept_metrics = defaultdict(lambda: {"total": 0, "approved": 0, "rejected": 0, "pending": 0})
    
    for req in all_requests:
        dept = emp_dept_map.get(req.employee_id, "Unknown")
        dept_metrics[dept]["total"] += 1
        dept_metrics[dept][req.status.lower()] = dept_metrics[dept].get(req.status.lower(), 0) + 1
    
    comparison = {}
    for dept, metrics in dept_metrics.items():
        comparison[dept] = {
            **metrics,
            "approval_rate": metrics["approved"] / metrics["total"] if metrics["total"] > 0 else 0
        }
    
    return {"departments": comparison}


async def get_top_requesters(limit: int = 5) -> dict:
    """Get top N employees by request count."""
    all_requests = await request_service.get_all_requests()
    all_employees = await employee_service.get_all_employee()
    
    emp_counts = defaultdict(int)
    for req in all_requests:
        emp_counts[req.employee_id] += 1
    
    sorted_emps = sorted(emp_counts.items(), key=lambda x: x[1], reverse=True)[:limit]
    
    emp_map = {emp.employee_id: emp for emp in all_employees}
    
    leaderboard = []
    for emp_id, count in sorted_emps:
        emp = emp_map.get(emp_id)
        leaderboard.append({
            "employee_id": emp_id,
            "name": emp.name if emp else "Unknown",
            "department": emp.department if emp else "Unknown",
            "request_count": count
        })
    
    return {"top_requesters": leaderboard}


async def get_request_status_distribution() -> dict:
    """Get distribution of requests across all statuses."""
    all_requests = await request_service.get_all_requests()
    status_counts = defaultdict(int)
    
    for req in all_requests:
        status_counts[req.status] += 1
    
    total = len(all_requests)
    distribution = {
        status: {
            "count": count,
            "percentage": round((count / total * 100), 2) if total > 0 else 0
        }
        for status, count in status_counts.items()
    }
    
    return {"total_requests": total, "distribution": distribution}


async def search_requests_by_keyword(keyword: str) -> dict:
    """Search requests by keyword in request_id, type, or status."""
    all_requests = await request_service.get_all_requests()
    keyword_lower = keyword.lower()
    
    matches = [
        req for req in all_requests
        if keyword_lower in req.request_id.lower() or
           keyword_lower in req.type.lower() or
           keyword_lower in req.status.lower()
    ]
    
    return {"keyword": keyword, "matches": len(matches), "results": matches}


async def get_approver_performance() -> dict:
    """Analyze performance metrics for all approvers."""
    all_requests = await request_service.get_all_requests()
    
    approver_stats = defaultdict(lambda: {"total_assigned": 0, "approved": 0, "rejected": 0})
    
    for req in all_requests:
        if req.approver_by and req.approver_by.lower() != "none":
            approver_stats[req.approver_by]["total_assigned"] += 1
            if req.status.lower() == "approved":
                approver_stats[req.approver_by]["approved"] += 1
            elif req.status.lower() == "rejected":
                approver_stats[req.approver_by]["rejected"] += 1
    
    performance = {}
    for approver, stats in approver_stats.items():
        performance[approver] = {
            **stats,
            "approval_rate": stats["approved"] / stats["total_assigned"] if stats["total_assigned"] > 0 else 0
        }
    
    return {"approver_performance": performance}
