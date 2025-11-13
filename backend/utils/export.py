"""Data export utilities"""
import csv
import json
from io import StringIO
from typing import List, Dict

def export_to_csv(data: List[Dict], fields: List[str]) -> str:
    output = StringIO()
    writer = csv.DictWriter(output, fieldnames=fields)
    writer.writeheader()
    writer.writerows(data)
    return output.getvalue()

def export_to_json(data: List[Dict]) -> str:
    return json.dumps(data, indent=2, default=str)

def generate_report(requests: List, employees: List) -> Dict:
    total_requests = len(requests)
    status_counts = {}
    type_counts = {}
    
    for req in requests:
        status_counts[req.status] = status_counts.get(req.status, 0) + 1
        type_counts[req.type] = type_counts.get(req.type, 0) + 1
    
    return {
        "generated_at": str(datetime.now()),
        "summary": {
            "total_requests": total_requests,
            "total_employees": len(employees),
            "status_breakdown": status_counts,
            "type_breakdown": type_counts
        }
    }

from datetime import datetime
