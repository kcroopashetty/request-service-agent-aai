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
