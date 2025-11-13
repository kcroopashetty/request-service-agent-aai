import ApiService from "../services/apiService.js";
import notify from "../utils/notifications.js";
import desktopNotify from "../utils/desktop-notifications.js";
import theme from "../utils/theme.js";
import { exportToCSV } from "../utils/export.js";
import { calculateStats } from "../utils/stats.js";
import { celebrateSuccess } from "../utils/animations.js";
import { setupKeyboardShortcuts } from "../utils/shortcuts.js";
import { searchRequests, filterByStatus, filterByType, sortRequests } from "../utils/search.js";

let allRequests = [];
let filteredRequests = [];
let displayedCount = 10;
const LOAD_MORE_COUNT = 10;

// Loading Bar
function showLoadingBar() {
    const bar = document.getElementById('loading-bar');
    if (bar) {
        bar.style.width = '0%';
        bar.classList.add('loading');
        setTimeout(() => bar.style.width = '100%', 10);
    }
}

function hideLoadingBar() {
    const bar = document.getElementById('loading-bar');
    if (bar) {
        setTimeout(() => {
            bar.style.width = '0%';
            bar.classList.remove('loading');
        }, 300);
    }
}

const TYPE_ICONS = {
    laptop: '💻',
    mobile: '📱',
    travel: '✈️',
    expense: '💰'
};

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
    showLoadingSkeleton();
    showLoadingBar();

    try {
        const [requests, employeeMap] = await Promise.all([
            ApiService.get("/request/"),
            getEmployeeMap(),
        ]);

        allRequests = requests;
        filteredRequests = requests;
        renderRequests(requests, employeeMap);
    } catch (error) {
        console.error("Error loading requests:", error);
        requestList.innerHTML = `<p class="error">⚠️ Failed to load requests.</p>`;
    } finally {
        hideLoadingBar();
    }
}

function showLoadingSkeleton() {
    const requestList = document.getElementById("request-list");
    requestList.innerHTML = Array(3).fill(0).map(() => `
        <div class="skeleton-card">
            <div class="skeleton-header">
                <div class="skeleton-text skeleton-title"></div>
                <div class="skeleton-text skeleton-badge"></div>
            </div>
            <div class="skeleton-line"></div>
            <div class="skeleton-line"></div>
            <div class="skeleton-line short"></div>
        </div>
    `).join('');
}

function showEmptyState() {
    const requestList = document.getElementById("request-list");
    requestList.innerHTML = `
        <div class="empty-state">
            <i class="fa fa-inbox" style="font-size: 4rem; color: var(--color-border); margin-bottom: 1rem;"></i>
            <h3>No Requests Found</h3>
            <p>Create your first request to get started</p>
            <button onclick="document.getElementById('create-btn').click()" class="primary-btn" style="margin-top: 1rem;">
                <i class="fa fa-plus"></i> Create Request
            </button>
        </div>
    `;
}

function renderRequests(requests, employeeMap, append = false) {
    const requestList = document.getElementById("request-list");
    
    if (!append) {
        requestList.innerHTML = "";
        displayedCount = LOAD_MORE_COUNT;
    }

    if (requests.length === 0) {
        showEmptyState();
        return;
    }

    const itemsToShow = requests.slice(0, displayedCount);

    if (!append) {
        requestList.innerHTML = "";
    }

    itemsToShow.forEach((req, index) => {
        if (append && index < displayedCount - LOAD_MORE_COUNT) return;
            const employee = employeeMap[req.employee_id];
            const approver = employeeMap[req.approver_by];

            const item = document.createElement("div");
            item.classList.add("request-item");

            item.innerHTML = `
        <div class="request-header">
            <div style="display: flex; align-items: center; gap: 0.5rem;">
                <span class="type-icon">${TYPE_ICONS[req.type] || '📄'}</span>
                <span class="request-id">${req.request_id}</span>
            </div>
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
            <button class="delete-btn" data-id="${req.request_id}" title="Delete request">🗑 Delete</button>
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
                    if (!confirm(`Delete ${id}?`)) return;
                    await ApiService.delete(`/request/${id}`);
                    notify.success("Request deleted successfully!");
                    desktopNotify.notify('Request Deleted', { body: `${id} has been deleted` });
                    await loadRequests();
                    await displayStats();
                } catch (error) {
                    console.error("Error deleting request:", error);
                    notify.error("Failed to delete request.");
                }
            });
        });

        // Attach edit listeners
        document.querySelectorAll(".edit-btn").forEach((btn) => {
        btn.addEventListener("click", (e) => openEditModal(e.target.dataset.id));
    });

    showLoadMoreButton(requests.length);
}

function showLoadMoreButton(totalItems) {
    const paginationContainer = document.getElementById('pagination');
    if (!paginationContainer) return;

    if (displayedCount >= totalItems) {
        paginationContainer.innerHTML = '';
        return;
    }

    paginationContainer.innerHTML = `
        <div style="text-align: center; padding: 2rem;">
            <button class="primary-btn" onclick="loadMoreRequests()">
                <i class="fa fa-arrow-down"></i> Load More (${totalItems - displayedCount} remaining)
            </button>
        </div>
    `;
}

window.loadMoreRequests = async function() {
    displayedCount += LOAD_MORE_COUNT;
    const employeeMap = await getEmployeeMap();
    renderRequests(filteredRequests, employeeMap, true);
}

// ---------- Generate Request ID ----------
async function generateRequestId() {
    const requests = await ApiService.get("/request/");
    const maxId = requests.reduce((max, req) => {
        const num = parseInt(req.request_id.replace('REQ-', ''));
        return num > max ? num : max;
    }, 0);
    return `REQ-${String(maxId + 1).padStart(3, '0')}`;
}

// ---------- Create New Request ----------
function setupCreateModal() {
    const modal = document.getElementById("create-modal");
    const openBtn = document.getElementById("create-btn");
    const cancelBtn = document.getElementById("cancel-btn");
    const form = document.getElementById("create-form");

    openBtn.addEventListener("click", async () => {
        await populateEmployeeSelect("employee_id");
        const newId = await generateRequestId();
        document.getElementById("request_id").value = newId;
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

        try {
            await ApiService.post("/request/", newRequest);
            notify.success("Request created successfully!");
            desktopNotify.notify('New Request Created', { body: `${newRequest.request_id} - ${newRequest.type}` });
            modal.style.display = "none";
            form.reset();
            await loadRequests();
            await displayStats();
        } catch (error) {
            console.error("Error creating request:", error);
            notify.error("Failed to create request.");
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
            const request = await ApiService.get(`/request/`);
            const oldStatus = request.find(r => r.request_id === requestId)?.status;
            
            await ApiService.put(`/request/${requestId}`, updatedRequest);
            notify.success("Request updated successfully!");
            desktopNotify.notify('Request Updated', { body: `${updatedRequest.request_id} status: ${updatedRequest.status}` });
            
            if (oldStatus !== 'approved' && updatedRequest.status === 'approved') {
                celebrateSuccess();
            }
            
            modal.style.display = "none";
            await loadRequests();
            await displayStats();
        } catch (error) {
            console.error("Error updating request:", error);
            notify.error("Failed to update request.");
        }
    };

    document.getElementById("edit-cancel-btn").onclick = () => {
        modal.style.display = "none";
    };
}

// ---------- Stats Display ----------
async function displayStats() {
    try {
        const requests = await ApiService.get("/request/");
        const stats = calculateStats(requests);
        
        const statsContainer = document.getElementById("stats-container");
        if (statsContainer) {
            statsContainer.innerHTML = `
                <div class="stat-card" data-filter="all" style="cursor: pointer;">
                    <span class="stat-value">${stats.total}</span>
                    <span class="stat-label">Total</span>
                </div>
                <div class="stat-card" data-filter="pending" style="cursor: pointer;">
                    <span class="stat-value">${stats.pending}</span>
                    <span class="stat-label">Pending</span>
                </div>
                <div class="stat-card" data-filter="approved" style="cursor: pointer;">
                    <span class="stat-value">${stats.approved}</span>
                    <span class="stat-label">Approved</span>
                </div>
                <div class="stat-card" data-filter="rejected" style="cursor: pointer;">
                    <span class="stat-value">${stats.rejected}</span>
                    <span class="stat-label">Rejected</span>
                </div>
            `;
            
            document.querySelectorAll('.stat-card').forEach(card => {
                card.addEventListener('click', () => {
                    const filter = card.dataset.filter;
                    if (window.filterByStatusValue) {
                        window.filterByStatusValue(filter);
                    }
                    card.style.transform = 'scale(0.95)';
                    setTimeout(() => card.style.transform = '', 200);
                });
            });
        }

    } catch (error) {
        console.error("Error loading stats:", error);
    }
}



function getPeakRequestTime(requests) {
    const hours = {};
    requests.forEach(r => {
        const hour = new Date(r.created_at || new Date()).getHours();
        hours[hour] = (hours[hour] || 0) + 1;
    });
    
    const peak = Object.entries(hours).sort((a, b) => b[1] - a[1])[0];
    if (!peak) return 'N/A';
    
    const hour = parseInt(peak[0]);
    const period = hour >= 12 ? 'PM' : 'AM';
    const displayHour = hour > 12 ? hour - 12 : hour === 0 ? 12 : hour;
    return `${displayHour}:00 ${period}`;
}

// ---------- Stats Modal ----------
let statsModalChart = null;
let typeModalChart = null;

function openStatsModal(requests) {
    const modal = document.getElementById('stats-modal');
    const leaderboardModalEl = document.getElementById('leaderboard-modal');
    const predictionsModalEl = document.getElementById('predictions-modal');
    
    const statusData = {
        pending: requests.filter(r => r.status === 'pending').length,
        approved: requests.filter(r => r.status === 'approved').length,
        rejected: requests.filter(r => r.status === 'rejected').length,
        cancelled: requests.filter(r => r.status === 'cancelled').length
    };
    
    const typeData = {
        laptop: requests.filter(r => r.type === 'laptop').length,
        mobile: requests.filter(r => r.type === 'mobile').length,
        travel: requests.filter(r => r.type === 'travel').length,
        expense: requests.filter(r => r.type === 'expense').length
    };
    
    const total = requests.length;
    
    if (statsModalChart) statsModalChart.destroy();
    if (typeModalChart) typeModalChart.destroy();
    
    const statusCtx = document.getElementById('stats-modal-chart');
    statsModalChart = new Chart(statusCtx, {
        type: 'doughnut',
        data: {
            labels: ['Pending', 'Approved', 'Rejected', 'Cancelled'],
            datasets: [{
                data: [statusData.pending, statusData.approved, statusData.rejected, statusData.cancelled],
                backgroundColor: ['#fbbf24', '#10b981', '#ef4444', '#6b7280'],
                borderWidth: 0
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            plugins: {
                legend: { position: 'bottom', labels: { padding: 10, font: { size: 11 } } }
            }
        }
    });
    
    const typeCtx = document.getElementById('type-modal-chart');
    typeModalChart = new Chart(typeCtx, {
        type: 'pie',
        data: {
            labels: ['💻 Laptop', '📱 Mobile', '✈️ Travel', '💰 Expense'],
            datasets: [{
                data: [typeData.laptop, typeData.mobile, typeData.travel, typeData.expense],
                backgroundColor: ['#6366f1', '#818cf8', '#a5b4fc', '#c7d2fe'],
                borderWidth: 0
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            plugins: {
                legend: { position: 'bottom', labels: { padding: 10, font: { size: 11 } } }
            }
        }
    });
    

    
    // Render leaderboard in modal
    const employeeCounts = {};
    const employeeMap = {};
    
    requests.forEach(req => {
        employeeCounts[req.employee_id] = (employeeCounts[req.employee_id] || 0) + 1;
    });
    
    ApiService.get('/employee/').then(employees => {
        employees.forEach(emp => {
            employeeMap[emp.employee_id] = emp.name;
        });
        
        const sorted = Object.entries(employeeCounts)
            .sort((a, b) => b[1] - a[1])
            .slice(0, 5);
        
        if (leaderboardModalEl) {
            leaderboardModalEl.innerHTML = sorted.map(([empId, count], index) => `
                <div class="leaderboard-item">
                    <span class="leaderboard-rank">#${index + 1}</span>
                    <span class="leaderboard-name">${employeeMap[empId] || empId}</span>
                    <span class="leaderboard-count">${count}</span>
                </div>
            `).join('') || '<p style="color: var(--color-subtext);">No data available</p>';
        }
    });
    
    // Render predictions in modal
    const now = new Date();
    const thisMonth = requests.filter(r => {
        const created = new Date(r.created_at || now);
        return created.getMonth() === now.getMonth();
    });
    
    const approvalRate = requests.length > 0 
        ? ((requests.filter(r => r.status === 'approved').length / requests.length) * 100).toFixed(1)
        : 0;
    
    const avgPerMonth = requests.length > 0 ? (requests.length / 12).toFixed(1) : 0;
    const trend = thisMonth.length > avgPerMonth ? 'up' : 'down';
    const trendPercent = avgPerMonth > 0 
        ? Math.abs(((thisMonth.length - avgPerMonth) / avgPerMonth) * 100).toFixed(1)
        : 0;
    
    const peakHour = getPeakRequestTime(requests);
    
    if (predictionsModalEl) {
        predictionsModalEl.innerHTML = `
            <div class="insight-metric">
                <span class="insight-label">Approval Rate</span>
                <span class="insight-value">${approvalRate}%</span>
            </div>
            <div class="insight-metric">
                <span class="insight-label">This Month</span>
                <span class="insight-value">${thisMonth.length}</span>
            </div>
            <div class="insight-trend ${trend === 'up' ? 'trend-up' : 'trend-down'}">
                <i class="fa fa-arrow-${trend}"></i>
                ${trendPercent}% ${trend === 'up' ? 'increase' : 'decrease'} from average
            </div>
            <div class="insight-trend">
                <i class="fa fa-clock"></i>
                Peak request time: ${peakHour}
            </div>
        `;
    }
    
    modal.style.display = 'flex';
}

function setupStatsModal() {
    const modal = document.getElementById('stats-modal');
    const closeBtn = document.getElementById('stats-modal-close');
    
    closeBtn.addEventListener('click', () => {
        modal.style.display = 'none';
    });
    
    modal.addEventListener('click', (e) => {
        if (e.target === modal) {
            modal.style.display = 'none';
        }
    });
}

// ---------- Export Functionality ----------
function setupExport() {
    const exportBtn = document.getElementById("export-btn");
    if (exportBtn) {
        exportBtn.addEventListener("click", async () => {
            try {
                const requests = await ApiService.get("/request/");
                exportToCSV(requests, `requests_${new Date().toISOString().split('T')[0]}.csv`);
                notify.success("Data exported successfully!");
            } catch (error) {
                notify.error("Failed to export data.");
            }
        });
    }
}



// ---------- Analytics Button ----------
function setupAnalyticsButton() {
    const analyticsBtn = document.getElementById('analytics-btn');
    if (analyticsBtn) {
        analyticsBtn.addEventListener('click', async () => {
            const requests = await ApiService.get('/request/');
            openStatsModal(requests);
        });
    }
}

// ---------- Theme Toggle ----------
function setupThemeToggle() {
    const themeBtn = document.getElementById("theme-toggle");
    if (themeBtn) {
        themeBtn.addEventListener("click", () => {
            const newTheme = theme.toggle();
            themeBtn.innerHTML = newTheme === 'dark' ? '<i class="fa fa-sun"></i>' : '<i class="fa fa-moon"></i>';
        });
    }
}

// ---------- Desktop Notifications Toggle ----------
function setupNotificationToggle() {
    const notifBtn = document.getElementById('notification-toggle');
    if (notifBtn) {
        notifBtn.classList.toggle('active', desktopNotify.isEnabled());
        notifBtn.addEventListener('click', async () => {
            const enabled = await desktopNotify.toggle();
            notifBtn.classList.toggle('active', enabled);
            notify.info(enabled ? 'Desktop notifications enabled' : 'Desktop notifications disabled');
        });
    }
}

// ---------- Filter by Status ----------
function setupStatusFilter() {
    window.filterByStatusValue = async (status) => {
        const employeeMap = await getEmployeeMap();
        let results = status === 'all' ? [...allRequests] : allRequests.filter(r => r.status === status);
        filteredRequests = results;
        displayedCount = LOAD_MORE_COUNT;
        renderRequests(results, employeeMap);
    };
}

// ---------- Keyboard Shortcuts ----------
function setupShortcuts() {
    setupKeyboardShortcuts({
        newRequest: () => document.getElementById('create-btn')?.click(),
        export: () => document.getElementById('export-btn')?.click(),
        toggleTheme: () => document.getElementById('theme-toggle')?.click(),
        closeModal: () => {
            document.getElementById('create-modal').style.display = 'none';
            document.getElementById('edit-modal').style.display = 'none';
        }
    });
}

// ---------- Initialize ----------
window.addEventListener("DOMContentLoaded", () => {
    loadRequests();
    setupCreateModal();
    setupStatsModal();
    displayStats();
    setupExport();
    setupAnalyticsButton();
    setupThemeToggle();
    setupNotificationToggle();
    setupStatusFilter();
    setupShortcuts();
    
    if (desktopNotify.permission === 'default') {
        setTimeout(() => {
            if (confirm('Enable desktop notifications for request updates?')) {
                desktopNotify.requestPermission();
            }
        }, 2000);
    }
});
