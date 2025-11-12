import aiosqlite
from typing import List
from fastapi import HTTPException
from models.request_model import Request
from repo.request_repo import RequestRepo


class RequestService:
    def __init__(self, repo: RequestRepo):
        self.repo = repo

    async def create_request(self, req: Request) -> Request:
        await self.repo.init_db()
        await self.repo.create_request(req)
        return req

    async def get_all_requests(self) -> List[Request]:
        """Ignore SQL query string; just return all Requests."""
        await self.repo.init_db()
        return await self.repo.get_all_requests()

    async def get_request_by_employee_id(self, employee_id: str) -> List[Request]:
        await self.repo.init_db()
        return await self.repo.get_request_by_employee_id(employee_id)

    async def delete_request(self, request_id: str) -> bool:
        await self.repo.init_db()
        return await self.repo.delete_request(request_id)

    async def update_request(self, request_id: str, req: Request) -> Request:
        await self.repo.init_db()
        updated = await self.repo.update_request(request_id, req)
        if not updated:
            raise HTTPException(status_code=404, detail="Request not found to update")
        return req
