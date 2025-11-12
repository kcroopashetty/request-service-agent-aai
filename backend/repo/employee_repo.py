import aiosqlite
from typing import List, Optional
from fastapi import HTTPException
from models.employee_model import Employee
from constants import DB_NAME, EMPLOYEE_TABLE_NAME


class EmployeeRepo:
    def __init__(self, db_path: str = DB_NAME):
        self.db_path = db_path

    async def init_db(self):
        """Initialize table if not exists."""
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute(
                f"""
                CREATE TABLE IF NOT EXISTS {EMPLOYEE_TABLE_NAME} (
                    employee_id TEXT PRIMARY KEY,
                    name TEXT,
                    email TEXT,
                    department TEXT
                )
            """
            )
            await db.commit()

    async def create_employee(self, employee: Employee) -> Employee:
        if isinstance(employee, dict):
            employee = Employee(**employee)
        async with aiosqlite.connect(self.db_path) as db:
            try:
                await db.execute(
                    f"""
                    INSERT INTO {EMPLOYEE_TABLE_NAME} (employee_id, name, email, department)
                    VALUES (?, ?, ?, ?)
                """,
                    (
                        employee.employee_id,
                        employee.name,
                        employee.email,
                        employee.department,
                    ),
                )
                await db.commit()
                return employee
            except aiosqlite.IntegrityError:
                raise HTTPException(status_code=409, detail="Employee already exists")

    async def get_all_empoyees(self) -> List[Employee]:
        """Ignore SQL query string; just return all Employee."""
        async with aiosqlite.connect(self.db_path) as db:
            cursor = await db.execute(f"SELECT * FROM {EMPLOYEE_TABLE_NAME}")
            rows = await cursor.fetchall()
            employees = [
                Employee(
                    employee_id=row[0],
                    name=row[1],
                    email=row[2],
                    department=row[3],
                )
                for row in rows
            ]
            return employees

    async def get_employee_by_email(self, email: str) -> List[Employee]:
        async with aiosqlite.connect(self.db_path) as db:
            cursor = await db.execute(
                f"""
                SELECT * FROM {EMPLOYEE_TABLE_NAME} WHERE email = ?
            """,
                (email,),
            )
            rows = await cursor.fetchall()
            if not rows:
                raise HTTPException(status_code=404, detail="Employee not found")

            return [
                Employee(
                    employee_id=row[0],
                    name=row[1],
                    email=row[2],
                    department=row[3],
                )
                for row in rows
            ]

    async def delete_employee(self, employee_id: str) -> bool:
        async with aiosqlite.connect(self.db_path) as db:
            cursor = await db.execute(
                f"""
                DELETE FROM {EMPLOYEE_TABLE_NAME} WHERE employee_id = ?
            """,
                (employee_id,),
            )
            await db.commit()
            if cursor.rowcount == 0:
                raise HTTPException(status_code=404, detail="Employee not found")
            return True

    async def update_employee(self, employee_id: str, employee: Employee) -> Employee:
        if isinstance(employee, dict):
            employee = Employee(**employee)

        async with aiosqlite.connect(self.db_path) as db:
            try:
                cursor = await db.execute(
                    f"""
                    UPDATE {EMPLOYEE_TABLE_NAME}
                    SET name = ?,
                        email = ?,
                        department = ?
                    WHERE employee_id = ?
                    """,
                    (
                        employee.name,
                        employee.email,
                        employee.department,
                        employee_id,
                    ),
                )
                await db.commit()

                if cursor.rowcount == 0:
                    raise HTTPException(status_code=404, detail="Employee not found")

                return employee

            except Exception as e:
                raise HTTPException(
                    status_code=500, detail=f"Error updating employee: {str(e)}"
                )
