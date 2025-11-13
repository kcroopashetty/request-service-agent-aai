# Challenge 5 - Testing Guide

## Test Scenarios

### Test 1: Department with Highest Approval Rate
**Query**: "Which department has the highest approval rate?"

**Expected**: 
- Agent calls `get_department_with_highest_approval_rate()`
- Combines Employee and Request data
- Calculates approval rates per department
- Returns department with highest rate

**Sample Response**: 
```
Engineering has the highest approval rate at 100% (1 approved out of 1 total).

Complete breakdown:
- Engineering: 100% (1/1)
- IT Support: 100% (1/1)
- Finance: 0% (0/1)
- Human Resources: 0% (0/1)
- Sales: 0% (0/1)
```

---

### Test 2: Employee with Most Rejected Requests
**Query**: "Which employee has the most rejected requests?"

**Expected**:
- Agent calls `get_employee_with_most_rejected_requests()`
- Combines Employee and Request data
- Counts rejected requests per employee
- Returns employee with most rejections

**Sample Response**:
```
Rohan Mehta (EMP-003) from Human Resources has the most rejected requests with 1 rejection.
```

---

## Query Variations

### Highest Approval Rate:
- "What department has the best approval rate?"
- "Which department gets approved the most?"
- "Show me approval rates by department"

### Most Rejected:
- "Who has the most rejected requests?"
- "Which employee gets rejected the most?"
- "Show me rejection statistics by employee"

---

## Verification Checklist

- [ ] Agent combines Employee and Request models
- [ ] Approval rates are calculated correctly
- [ ] Employee details are enriched (name, department)
- [ ] Agent provides detailed breakdowns
- [ ] Agent handles edge cases (no data, ties)

---

## Sample Data Analysis

Based on `backend/data/`:

**Requests by Department**:
- Engineering (EMP-001): REQ-001 (approved) → 100%
- Finance (EMP-002): REQ-002 (pending) → 0%
- Human Resources (EMP-003): REQ-003 (rejected) → 0%
- IT Support (EMP-004): REQ-004 (approved) → 100%
- Sales (EMP-005): REQ-005 (pending) → 0%

**Rejected Requests**:
- EMP-003 (Rohan Mehta): 1 rejection
- All others: 0 rejections
