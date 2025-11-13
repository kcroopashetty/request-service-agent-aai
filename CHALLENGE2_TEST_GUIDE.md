# Challenge 2 - Testing Guide

## Quick Start

1. Start the backend:
   ```bash
   cd backend
   python main.py
   ```

2. Open chat interface at your workspace URL

3. Try the test queries below

---

## Test Scenarios

### Test 1: Add Request
**Query**: "Add a travel request REQ-006 for employee EMP-001 with status pending and approver EMP-004"

**Expected**: 
- Agent calls `add_request()`
- Request is created in database
- Confirmation message returned

**Variations**:
- "Create a laptop request REQ-007 for EMP-002"
- "Add expense request REQ-008 for employee EMP-003"

---

### Test 2: Add Employee
**Query**: "Add employee EMP-006 named John Doe with email john.doe@company.com in Engineering department"

**Expected**:
- Agent calls `add_employee()`
- Employee record created
- Confirmation message

**Variations**:
- "Create employee EMP-007 named Jane Smith, email jane@company.com, department Finance"
- "Add new employee EMP-008, name Bob Wilson, email bob@company.com, IT Support"

---

### Test 3: Filter Requests by Type
**Query**: "Which requests are of type travel?"

**Expected**:
- Agent calls `fetch_requests_by_type("travel")`
- Returns REQ-003, REQ-005 (from sample data)
- Shows request details

**Variations**:
- "Show me all laptop requests"
- "List expense requests"
- "What mobile requests do we have?"

---

### Test 4: List Pending Requests
**Query**: "List all pending requests"

**Expected**:
- Agent calls `fetch_pending_requests()`
- Returns REQ-002, REQ-005 (from sample data)
- Shows pending request details

**Variations**:
- "Show pending requests"
- "What requests are pending?"
- "Which requests need approval?"

---

### Test 5: Check Request by Employee
**Query**: "Is there a request raised by EMP-001?"

**Expected**:
- Agent calls `fetch_request_by_employee_id("EMP-001")`
- Returns REQ-001 (laptop request)
- Shows request details

**Variations**:
- "Show requests for employee EMP-002"
- "What requests did EMP-003 raise?"
- "List all requests from EMP-004"

---

### Test 6: Update Request Status
**Query**: "Update the status of request REQ-002 to approved"

**Expected**:
- Agent calls `update_request_status("REQ-002", "approved")`
- Status updated in database
- Confirmation message

**Variations**:
- "Change REQ-005 status to rejected"
- "Mark request REQ-003 as cancelled"
- "Approve request REQ-004"

---

### Test 7: Delete Request
**Query**: "Remove request REQ-003 from the list"

**Expected**:
- Agent calls `delete_request("REQ-003")`
- Request deleted from database
- Success confirmation

**Variations**:
- "Delete request REQ-005"
- "Remove REQ-002 from database"
- "Cancel and delete request REQ-001"

---

## Combined Operations Test

**Query**: "Add a travel request REQ-010 for EMP-001, then show me all travel requests"

**Expected**:
- Agent calls `add_request()` first
- Then calls `fetch_requests_by_type("travel")`
- Shows updated list including new request

---

## Sample Data Reference

From `backend/data/request_data.py`:
- REQ-001: laptop, approved, EMP-001
- REQ-002: expense, pending, EMP-002
- REQ-003: travel, rejected, EMP-003
- REQ-004: mobile, approved, EMP-004
- REQ-005: travel, pending, EMP-005

From `backend/data/employee_data.py`:
- EMP-001: Aarav Sharma, Engineering
- EMP-002: Priya Nair, Finance
- EMP-003: Rohan Mehta, Human Resources
- EMP-004: Isha Verma, IT Support
- EMP-005: Vikram Singh, Sales

---

## Verification Checklist

- [ ] Can add new requests
- [ ] Can add new employees
- [ ] Can filter requests by type (travel, laptop, mobile, expense)
- [ ] Can list pending requests
- [ ] Can check requests by employee ID
- [ ] Can update request status
- [ ] Can delete requests
- [ ] Agent understands natural language variations
- [ ] Responses are clear and accurate

---

## Troubleshooting

**Issue**: "Request not found"
- Verify request ID exists in database
- Check spelling of request ID

**Issue**: "Employee not found"
- Verify employee ID exists
- Check employee data in database

**Issue**: Tool not called
- Rephrase query more clearly
- Be specific with parameters (IDs, types, status)
