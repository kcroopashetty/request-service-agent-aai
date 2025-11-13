"""
Demo Data Seeder for Hebbale Academy Challenges
Run this to populate database with test data for all challenge queries
"""

import sqlite3
from datetime import datetime, timedelta
import random

def seed_demo_data():
    conn = sqlite3.connect('request_service.db')
    cursor = conn.cursor()
    
    # Clear existing data
    cursor.execute("DELETE FROM request")
    cursor.execute("DELETE FROM employee")
    
    # Add Employees
    employees = [
        ("EMP001", "John Doe", "john@company.com", "Engineering"),
        ("EMP002", "Jane Smith", "jane@company.com", "Marketing"),
        ("EMP003", "Bob Wilson", "bob@company.com", "Engineering"),
        ("EMP004", "Alice Brown", "alice@company.com", "HR"),
        ("EMP005", "Charlie Davis", "charlie@company.com", "Finance"),
        ("EMP006", "Diana Miller", "diana@company.com", "Engineering"),
        ("EMP007", "Eve Taylor", "eve@company.com", "Marketing"),
    ]
    
    cursor.executemany(
        "INSERT INTO employee (employee_id, name, email, department) VALUES (?, ?, ?, ?)",
        employees
    )
    
    # Add Requests with varied data
    requests = [
        # Travel requests
        ("REQ001", "EMP001", "travel", "approved", "EMP004", (datetime.now() - timedelta(days=10)).isoformat()),
        ("REQ002", "EMP002", "travel", "approved", "EMP004", (datetime.now() - timedelta(days=8)).isoformat()),
        ("REQ003", "EMP006", "travel", "pending", "EMP004", (datetime.now() - timedelta(days=6)).isoformat()),
        
        # Laptop requests
        ("REQ004", "EMP001", "laptop", "approved", "EMP004", (datetime.now() - timedelta(days=15)).isoformat()),
        ("REQ005", "EMP003", "laptop", "approved", "EMP005", (datetime.now() - timedelta(days=12)).isoformat()),
        ("REQ006", "EMP006", "laptop", "rejected", "EMP004", (datetime.now() - timedelta(days=9)).isoformat()),
        
        # Expense requests
        ("REQ007", "EMP002", "expense", "approved", "EMP005", (datetime.now() - timedelta(days=7)).isoformat()),
        ("REQ008", "EMP003", "expense", "rejected", "EMP005", (datetime.now() - timedelta(days=5)).isoformat()),
        ("REQ009", "EMP007", "expense", "pending", "EMP005", (datetime.now() - timedelta(days=8)).isoformat()),
        
        # Mobile requests
        ("REQ010", "EMP001", "mobile", "approved", "EMP004", (datetime.now() - timedelta(days=3)).isoformat()),
        ("REQ011", "EMP006", "mobile", "rejected", "EMP004", (datetime.now() - timedelta(days=4)).isoformat()),
        
        # Desk phone requests
        ("REQ012", "EMP003", "desk_phone", "rejected", "EMP005", (datetime.now() - timedelta(days=11)).isoformat()),
        ("REQ013", "EMP007", "desk_phone", "pending", "EMP004", (datetime.now() - timedelta(days=2)).isoformat()),
        
        # Additional for testing
        ("REQ099", "EMP002", "travel", "cancelled", "EMP004", (datetime.now() - timedelta(days=20)).isoformat()),
        ("REQ102", "EMP003", "laptop", "pending", "EMP005", (datetime.now() - timedelta(days=1)).isoformat()),
    ]
    
    cursor.executemany(
        "INSERT INTO request (request_id, employee_id, type, status, approver_by) VALUES (?, ?, ?, ?, ?)",
        [(r[0], r[1], r[2], r[3], r[4]) for r in requests]
    )
    
    conn.commit()
    conn.close()
    
    print("✅ Demo data seeded successfully!")
    print(f"📊 Added {len(employees)} employees")
    print(f"📋 Added {len(requests)} requests")
    print("\n🎯 Ready for challenge queries!")
    print("\nTest queries:")
    print('1. "Which requests are of type travel?"')
    print('2. "List all pending requests"')
    print('3. "Is there a request raised by EMP001?"')
    print('4. "How many total requests are there?"')
    print('5. "Which department raised the most requests?"')

if __name__ == "__main__":
    seed_demo_data()
