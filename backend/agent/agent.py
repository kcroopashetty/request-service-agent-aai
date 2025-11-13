from google.adk.agents import LlmAgent
from .tools import (
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
    count_total_requests,
    count_requests_by_status,
    get_department_with_most_requests,
    get_most_recently_approved_request,
    get_pending_requests_older_than_days,
    get_approver_with_most_approvals,
    get_department_with_highest_approval_rate,
    get_employee_with_most_rejected_requests,
)
from constants import AGENT_NAME, AGENT_DESCRIPTION, AGENT_MODEL
from . import prompt


root_agent = LlmAgent(
    name=AGENT_NAME,
    model=AGENT_MODEL,
    description=AGENT_DESCRIPTION,
    instruction=prompt.ROOT_AGENT_PROMPT,
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
        count_total_requests,
        count_requests_by_status,
        get_department_with_most_requests,
        get_most_recently_approved_request,
        get_pending_requests_older_than_days,
        get_approver_with_most_approvals,
        get_department_with_highest_approval_rate,
        get_employee_with_most_rejected_requests,
    ],
)
