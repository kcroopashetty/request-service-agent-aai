# Challenge 3 - Testing Guide

## Test Scenarios

### Test 1: Count Total Requests
**Query**: "How many total requests are there?"

**Expected**: Agent calls `count_total_requests` and returns the total count.

**Sample Response**: "There are 5 total requests in the system."

---

### Test 2: Count Approved Requests
**Query**: "How many are in approved status?"

**Expected**: Agent calls `count_requests_by_status` with status="approved".

**Sample Response**: "There are 2 requests with approved status."

---

### Test 3: Department with Most Requests
**Query**: "Which department raised the most requests?"

**Expected**: Agent calls `get_department_with_most_requests` and provides detailed breakdown.

**Sample Response**: 
```
Engineering raised the most requests with 2 requests.

Here's the complete breakdown by department:
- Engineering: 2 requests
- Finance: 1 request
- Human Resources: 1 request
- IT Support: 1 request
- Sales: 1 request
```

---

## Additional Test Variations

### For Total Count:
- "What's the total number of requests?"
- "Count all requests"
- "How many requests do we have?"

### For Status Count:
- "How many pending requests?"
- "Count rejected requests"
- "How many requests are cancelled?"

### For Department Analysis:
- "What department has the most requests?"
- "Which department is most active?"
- "Show me request distribution by department"

---

## Combined Analytics Queries

Test the agent's ability to handle multiple analytics:

**Query**: "Give me a summary: total requests, approved count, and top department"

**Expected**: Agent should call all 3 tools and provide comprehensive summary.

---

## Verification Checklist

- [ ] Agent can count total requests
- [ ] Agent can count requests by any status (approved, pending, rejected, cancelled)
- [ ] Agent can identify department with most requests
- [ ] Agent provides detailed breakdown when appropriate
- [ ] Agent handles edge cases (no requests, tie between departments)
- [ ] Agent responds in human-readable format

---

## Sample Data Verification

Based on the sample data in `backend/data/`:
- Total requests: 5
- Approved: 2 (REQ-001, REQ-004)
- Pending: 2 (REQ-002, REQ-005)
- Rejected: 1 (REQ-003)
- Department breakdown:
  - Engineering: 1 (EMP-001)
  - Finance: 1 (EMP-002)
  - Human Resources: 1 (EMP-003)
  - IT Support: 1 (EMP-004)
  - Sales: 1 (EMP-005)
