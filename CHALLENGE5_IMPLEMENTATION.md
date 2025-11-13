# Challenge 5 - Multi-Modal Implementation

## Overview
Challenge 5 adds multi-modal capabilities that combine Employee and Request models to provide cross-model analytics.

## Tools Added

### 1. Department with Highest Approval Rate
```python
async def get_department_with_highest_approval_rate() -> dict
```
Combines Employee and Request data to calculate approval rates per department and identify the highest.

**Logic**:
- Maps employees to departments
- Counts total and approved requests per department
- Calculates approval rate (approved/total)
- Returns department with highest rate

### 2. Employee with Most Rejected Requests
```python
async def get_employee_with_most_rejected_requests() -> dict
```
Combines Employee and Request data to find which employee has the most rejected requests.

**Logic**:
- Counts rejected requests per employee
- Retrieves employee details (name, department)
- Returns employee with highest rejection count

## Multi-Modal Aspect
Both tools demonstrate multi-modal capabilities by:
- Working with multiple data models (Employee + Request)
- Joining data across models
- Providing enriched insights from combined data

## Expected Queries

1. "Which department has the highest approval rate?"
2. "Which employee has the most rejected requests?"

## Status
✅ Implementation Complete
