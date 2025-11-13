# Challenge 4 - Testing Guide

## Test Scenarios

### Test 1: Most Recently Approved Request
**Query**: "Which request was most recently approved?"

**Expected**: Agent calls `get_most_recently_approved_request()` and returns the request with latest approval timestamp.

**Sample Response**: "The most recently approved request is REQ-004 (mobile request by EMP-004, approved by EMP-003)."

---

### Test 2: Old Pending Requests
**Query**: "List all requests pending for more than 5 days"

**Expected**: Agent calls `get_pending_requests_older_than_days(5)` and returns matching requests.

**Sample Response**: "Found 2 requests pending for more than 5 days: REQ-002 (expense) and REQ-005 (travel)."

---

### Test 3: Top Approver
**Query**: "Which approver approved the most requests?"

**Expected**: Agent calls `get_approver_with_most_approvals()` and returns approver statistics.

**Sample Response**: "EMP-004 approved the most requests with 1 approval. Complete breakdown: EMP-004: 1, EMP-003: 1."

---

## Query Variations

### Most Recent Approval:
- "What's the latest approved request?"
- "Show me the most recent approval"
- "Which request was approved last?"

### Old Pending:
- "Show pending requests older than 5 days"
- "Which requests have been pending for over 5 days?"
- "List old pending requests"

### Top Approver:
- "Who approved the most requests?"
- "Which approver is most active?"
- "Show me approval statistics"

---

## Verification Checklist

- [ ] Agent can find most recently approved request
- [ ] Agent can filter pending requests by age
- [ ] Agent can identify top approver
- [ ] Agent provides detailed breakdowns
- [ ] Agent handles edge cases (no data)
- [ ] Timestamps are correctly compared

---

## Sample Data

Based on `backend/data/request_data.py`:
- Approved: REQ-001 (EMP-004), REQ-004 (EMP-003)
- Pending: REQ-002, REQ-005
- Approvers: EMP-004 (1), EMP-003 (1)
