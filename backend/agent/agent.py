from google.adk.agents import LlmAgent
from .tools import (
    fetch_all_employees,
    fetch_all_requests,
    fetch_employees_by_email,
    fetch_request_by_employee_id,
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
    ],
)
