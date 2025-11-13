# Challenge 2 - Implementation Guide

## Overview
Challenge 2 makes Request Service operations conversational by adding tools for CRUD operations (Create, Read, Update, Delete) on requests and employees.

## Implementation Details

### Tools Added to `backend/agent/tools.py`

#### 1. Add Request
```python
async def add_request(request_id: str, employee_id: str, type: str, status: str, approver_by: str) -> dict
```
- Creates a new request in the database
- Parameters: request_id, employee_id, type, status, approver_by
- Types: laptop, mobile, travel, expense
- Status: pending, approved, rejected, cancelled

#### 2. Add Employee
```python
async def add_employee(employee_id: str, name: str, email: str, department: str) -> dict
```
- Creates a new employee record
- Parameters: employee_id, name, email, department

#### 3. Fetch Requests by Type
```python
async def fetch_requests_by_type(type: str) -> dict
```
- Filters requests by type (travel, laptop, mobile, expense)
- Returns list of matching requests

#### 4. Fetch Pending Requests
```python
async def fetch_pending_requests() -> dict
```
- Returns all requests with status "pending"
- Useful for tracking pending approvals

#### 5. Update Request Status
```python
async def update_request_status(request_id: str, new_status: str) -> dict
```
- Updates the status of a specific request
- New status: pending, approved, rejected, cancelled

#### 6. Delete Request
```python
async def delete_request(request_id: str) -> dict
```
- Removes a request from the database
- Returns success confirmation

## Agent Configuration

All tools are registered in `backend/agent/agent.py`:
```python
root_agent = LlmAgent(
    tools=[
        fetch_all_employees,
        fetch_all_requests,
        fetch_employees_by_email,
        fetch_request_by_employee_id,
        add_request,
        add_employee,
        fetch_requests_by_type,
        fetch_pending_requests,
        update_request_status,
        delete_request,
    ]
)
```

## Prompt Updates

Updated `backend/agent/prompt.py` to include:
- Add new requests and employees
- Filter by type and status
- Update request status
- Delete requests

## Expected Queries

1. **Add Request**: "Add a travel request REQ-006 for employee EMP-001"
2. **Add Employee**: "Add employee EMP-006 named John Doe with email john@company.com in Engineering"
3. **Filter by Type**: "Which requests are of type travel?"
4. **List Pending**: "List all pending requests"
5. **Check by Employee**: "Is there a request raised by EMP-001?"
6. **Update Status**: "Update the status of request REQ-102 to approved"
7. **Delete Request**: "Remove request REQ-099 from the list"

## Status
✅ Implementation Complete
✅ Tools Registered
✅ Prompt Updated
✅ Ready for Testing
