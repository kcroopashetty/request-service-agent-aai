from typing import List
from fastapi import HTTPException
from models.employee_model import Employee
from repo.employee_repo import EmployeeRepo


class EmployeeService:
    def __init__(self, repo: EmployeeRepo):
        self.repo = repo

    async def create_employee(self, employee: Employee) -> Employee:
        await self.repo.init_db()
        await self.repo.create_employee(employee)
        return employee

    async def get_all_employee(self) -> List[Employee]:
        """Ignore SQL query string; just return all Employee."""
        await self.repo.init_db()
        return await self.repo.get_all_empoyees()

    async def get_employee_by_email(self, email: str) -> List[Employee]:
        await self.repo.init_db()
        return await self.repo.get_employee_by_email(email)

    async def update_employee(self, employee_id: str, employee: Employee) -> Employee:
        await self.repo.init_db()
        updated = await self.repo.update_employee(employee_id, employee)
        if not updated:
            raise HTTPException(status_code=404, detail="Employee not found to update")
        return employee

    async def delete_employee(self, employee_id: str) -> bool:
        await self.repo.init_db()
        return await self.repo.delete_employee(employee_id)
