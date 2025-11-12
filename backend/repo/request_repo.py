import aiosqlite
from typing import List, Optional
from fastapi import HTTPException
from models.request_model import Request
from constants import DB_NAME, REQUEST_TABLE_NAME


class RequestRepo:
    def __init__(self, db_path: str = DB_NAME):
        self.db_path = db_path

    async def init_db(self):
        """Initialize table if not exists."""
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute(
                f"""
                CREATE TABLE IF NOT EXISTS {REQUEST_TABLE_NAME} (
                    request_id TEXT PRIMARY KEY,
                    employee_id TEXT,
                    type TEXT,
                    status TEXT,
                    approver_by TEXT
                )
            """
            )
            await db.commit()

    async def create_request(self, request: Request) -> Request:
        if isinstance(request, dict):
            request = Request(**request)
        async with aiosqlite.connect(self.db_path) as db:
            try:
                await db.execute(
                    f"""
                    INSERT INTO {REQUEST_TABLE_NAME} (request_id, employee_id, type, status, approver_by)
                    VALUES (?, ?, ?, ?, ?)
                """,
                    (
                        request.request_id,
                        request.employee_id,
                        request.type,
                        request.status,
                        request.approver_by,
                    ),
                )
                await db.commit()
                return request
            except aiosqlite.IntegrityError:
                raise HTTPException(status_code=409, detail="Request already exists")

    async def get_all_requests(self) -> List[Request]:
        """Ignore SQL query string; just return all Requests."""
        async with aiosqlite.connect(self.db_path) as db:
            cursor = await db.execute(f"SELECT * FROM {REQUEST_TABLE_NAME}")
            rows = await cursor.fetchall()
            requests = [
                Request(
                    request_id=row[0],
                    employee_id=row[1],
                    type=row[2],
                    status=row[3],
                    approver_by=row[4],
                )
                for row in rows
            ]
            return requests

    async def get_request_by_employee_id(self, employee_id: str) -> List[Request]:
        async with aiosqlite.connect(self.db_path) as db:
            cursor = await db.execute(
                f"""
                SELECT * FROM {REQUEST_TABLE_NAME} WHERE employee_id = ?
            """,
                (employee_id,),
            )
            rows = await cursor.fetchall()
            if not rows:
                raise HTTPException(status_code=404, detail="Request not found")

            return [
                Request(
                    request_id=row[0],
                    employee_id=row[1],
                    type=row[2],
                    status=row[3],
                    approver_by=row[4],
                )
                for row in rows
            ]

    async def delete_request(self, request_id: str) -> bool:
        async with aiosqlite.connect(self.db_path) as db:
            cursor = await db.execute(
                f"""
                DELETE FROM {REQUEST_TABLE_NAME} WHERE request_id = ?
            """,
                (request_id,),
            )
            await db.commit()
            if cursor.rowcount == 0:
                raise HTTPException(status_code=404, detail="Request not found")
            return True

    async def update_request(self, request_id: str, request: Request) -> Request:
        if isinstance(request, dict):
            request = Request(**request)

        async with aiosqlite.connect(self.db_path) as db:
            try:
                cursor = await db.execute(
                    f"""
                    UPDATE {REQUEST_TABLE_NAME}
                    SET employee_id = ?,
                        type = ?,
                        status = ?,
                        approver_by = ?
                    WHERE request_id = ?
                    """,
                    (
                        request.employee_id,
                        request.type,
                        request.status,
                        request.approver_by,
                        request_id,
                    ),
                )
                await db.commit()

                if cursor.rowcount == 0:
                    raise HTTPException(status_code=404, detail="Request not found")

                return request

            except Exception as e:
                raise HTTPException(
                    status_code=500, detail=f"Error updating request: {str(e)}"
                )
