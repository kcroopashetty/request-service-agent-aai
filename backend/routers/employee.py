from fastapi import APIRouter, Depends, status
from typing import List, Optional
from models.employee_model import Employee
from services.employee_service import EmployeeService
from services import employee_service
from repo.employee_repo import EmployeeRepo
from constants import DB_NAME

router = APIRouter()
repo = EmployeeRepo(DB_NAME)
employee_service = EmployeeService(repo)


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_employee_endpoint(emp: Employee):
    await employee_service.create_employee(emp)
    return {"message": "Employee added successfully"}


@router.put("/{employee_id}", status_code=status.HTTP_200_OK)
async def update_employee_endpoint(employee_id: str, employee: Employee):
    """Update an existing employee record"""
    return await employee_service.update_employee(employee_id, employee)


@router.get("/", response_model=List[Employee], status_code=status.HTTP_200_OK)
async def search_employee_endpoint(email: Optional[str] = None):
    if email:
        return await employee_service.get_employee_by_email(email)
    else:
        return await employee_service.get_all_employee()


@router.delete("/{employee_id}")
async def delete_employee_endpoint(
    employee_id: str,
):
    await employee_service.delete_employee(employee_id)
    return {"message": "Employee deleted successfully"}
