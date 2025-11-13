import aiosqlite
from typing import List
from datetime import datetime
from models.approval_model import Approval

class ApprovalRepo:
    def __init__(self, db_name: str):
        self.db_name = db_name

    async def init_db(self):
        async with aiosqlite.connect(self.db_name) as db:
            await db.execute("""
                CREATE TABLE IF NOT EXISTS approvals (
                    approval_id TEXT PRIMARY KEY,
                    request_id TEXT NOT NULL,
                    approver_id TEXT NOT NULL,
                    approval_level INTEGER NOT NULL,
                    status TEXT NOT NULL,
                    comments TEXT,
                    approved_at TEXT,
                    created_at TEXT NOT NULL
                )
            """)
            await db.commit()

    async def create_approval(self, approval: Approval):
        async with aiosqlite.connect(self.db_name) as db:
            await db.execute(
                "INSERT INTO approvals VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                (approval.approval_id, approval.request_id, approval.approver_id,
                 approval.approval_level, approval.status, approval.comments,
                 approval.approved_at, approval.created_at)
            )
            await db.commit()

    async def get_pending_approvals(self, approver_id: str) -> List[Approval]:
        async with aiosqlite.connect(self.db_name) as db:
            db.row_factory = aiosqlite.Row
            async with db.execute(
                "SELECT * FROM approvals WHERE approver_id = ? AND status = 'pending'",
                (approver_id,)
            ) as cursor:
                rows = await cursor.fetchall()
                return [Approval(**dict(row)) for row in rows]

    async def update_approval_status(self, approval_id: str, status: str, comments: str = None):
        async with aiosqlite.connect(self.db_name) as db:
            await db.execute(
                "UPDATE approvals SET status = ?, comments = ?, approved_at = ? WHERE approval_id = ?",
                (status, comments, datetime.utcnow().isoformat(), approval_id)
            )
            await db.commit()
