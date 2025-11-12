import ApiService from "../services/apiService.js";

// ---------- Load Employees ----------
async function getEmployeeMap() {
    const employees = await ApiService.get("/employee/");
    return Object.fromEntries(employees.map(emp => [emp.employee_id, emp]));
}

async function populateEmployeeSelect(selectId, selectedId = "") {
    const select = document.getElementById(selectId);
    select.innerHTML = "<option value=''>-- Select Employee --</option>";

    try {
        const employees = await ApiService.get("/employee/");
        employees.forEach(emp => {
            const option = document.createElement("option");
            option.value = emp.employee_id;
            option.textContent = `${emp.name} (${emp.department})`;
            if (emp.employee_id === selectedId) option.selected = true;
            select.appendChild(option);
        });
    } catch (error) {
        console.error("Error loading employees:", error);
        select.innerHTML = "<option value=''>Failed to load employees</option>";
    }
}

// ---------- Load Requests ----------
async function loadRequests() {
    const requestList = document.getElementById("request-list");
    requestList.innerHTML = `<p>Loading requests...</p>`;

    try {
        const [requests, employeeMap] = await Promise.all([
            ApiService.get("/request/"),
            getEmployeeMap(),
        ]);

        requestList.innerHTML = "";

        if (requests.length === 0) {
            requestList.innerHTML = `<p>No requests found.</p>`;
            return;
        }

        requests.forEach((req) => {
            const employee = employeeMap[req.employee_id];
            const approver = employeeMap[req.approver_by];

            const item = document.createElement("div");
            item.classList.add("request-item");

            item.innerHTML = `
        <div class="request-header">
            <span class="request-id">${req.request_id}</span>
            <span class="request-status status-${req.status}">${req.status}</span>
        </div>
        <div class="request-details">
            <p><strong>Employee:</strong> ${employee ? employee.name : "Unknown"}</p>
            <p><strong>Type:</strong> ${req.type}</p>
            <p><strong>Approver:</strong> ${approver ? approver.name : "None"}</p>
            <p><strong>Department:</strong> ${employee ? employee.department : "-"}</p>
        </div>
        <div class="request-actions">
            <button class="edit-btn" data-id="${req.request_id}">✏️ Edit</button>
            <button class="delete-btn" data-id="${req.request_id}">🗑 Delete</button>
        </div>
      `;

            requestList.appendChild(item);
        });

        // Attach delete listeners
        document.querySelectorAll(".delete-btn").forEach((btn) => {
            btn.addEventListener("click", async (e) => {
                const id = e.target.dataset.id;
                // if (!confirm(`Are you sure you want to delete ${id}?`)) return;
                console.log("Deleted Successfully")
                try {
                    await ApiService.delete(`/request/${id}`);
                    alert("✅ Request deleted successfully!");
                    await loadRequests();
                } catch (error) {
                    console.error("Error deleting request:", error);
                    alert("❌ Failed to delete request.");
                }
            });
        });

        // Attach edit listeners
        document.querySelectorAll(".edit-btn").forEach((btn) => {
            btn.addEventListener("click", (e) => openEditModal(e.target.dataset.id));
        });

    } catch (error) {
        console.error("Error loading requests:", error);
        requestList.innerHTML = `<p class="error">⚠️ Failed to load requests.</p>`;
    }
}

// ---------- Create New Request ----------
function setupCreateModal() {
    const modal = document.getElementById("create-modal");
    const openBtn = document.getElementById("create-btn");
    const cancelBtn = document.getElementById("cancel-btn");
    const form = document.getElementById("create-form");

    openBtn.addEventListener("click", async () => {
        await populateEmployeeSelect("employee_id");
        modal.style.display = "flex";
    });

    cancelBtn.addEventListener("click", () => {
        modal.style.display = "none";
        form.reset();
    });

    form.addEventListener("submit", async (e) => {
        e.preventDefault();

        const newRequest = {
            request_id: document.getElementById("request_id").value.trim(),
            employee_id: document.getElementById("employee_id").value,
            type: document.getElementById("type").value,
            status: "pending",
            approver_by: "None",
        };

        if (!newRequest.request_id.startsWith("REQ-")) {
            alert("Request ID must start with 'REQ-' (e.g., REQ-006)");
            return;
        }

        try {
            const existingRequests = await ApiService.get("/request/");
            if (existingRequests.some((r) => r.request_id === newRequest.request_id)) {
                alert("⚠️ Request ID already exists. Please use a unique ID.");
                return;
            }

            await ApiService.post("/request/", newRequest);
            alert("✅ Request created successfully!");
            modal.style.display = "none";
            form.reset();
            await loadRequests();
        } catch (error) {
            console.error("Error creating request:", error);
            alert("❌ Failed to create request. Check console for details.");
        }
    });
}

// ---------- Edit Request Modal ----------
async function openEditModal(requestId) {
    const modal = document.getElementById("edit-modal");
    const form = document.getElementById("edit-form");

    try {
        const request = await ApiService.get(`/request/`);
        const reqData = request.find(r => r.request_id === requestId);
        if (!reqData) {
            alert("❌ Request not found.");
            return;
        }

        document.getElementById("edit_request_id").value = reqData.request_id;
        await populateEmployeeSelect("edit_employee_id", reqData.employee_id);
        document.getElementById("edit_type").value = reqData.type;
        document.getElementById("edit_status").value = reqData.status;
        document.getElementById("edit_approver_by").value = reqData.approver_by;

        modal.style.display = "flex";
    } catch (error) {
        console.error("Error loading request for edit:", error);
    }

    form.onsubmit = async (e) => {
        e.preventDefault();

        const updatedRequest = {
            request_id: document.getElementById("edit_request_id").value,
            employee_id: document.getElementById("edit_employee_id").value,
            type: document.getElementById("edit_type").value,
            status: document.getElementById("edit_status").value,
            approver_by: document.getElementById("edit_approver_by").value,
        };

        try {
            await ApiService.put(`/request/${requestId}`, updatedRequest);
            alert("✅ Request updated successfully!");
            modal.style.display = "none";
            await loadRequests();
        } catch (error) {
            console.error("Error updating request:", error);
            alert("❌ Failed to update request.");
        }
    };

    document.getElementById("edit-cancel-btn").onclick = () => {
        modal.style.display = "none";
    };
}

// ---------- Initialize ----------
window.addEventListener("DOMContentLoaded", () => {
    loadRequests();
    setupCreateModal();
});
