// Search and Filter Utilities
export function searchRequests(requests, query) {
    if (!query) return requests;
    
    const lowerQuery = query.toLowerCase();
    return requests.filter(req => 
        req.request_id.toLowerCase().includes(lowerQuery) ||
        req.employee_id.toLowerCase().includes(lowerQuery) ||
        req.type.toLowerCase().includes(lowerQuery) ||
        req.status.toLowerCase().includes(lowerQuery)
    );
}

export function filterByStatus(requests, status) {
    if (!status || status === 'all') return requests;
    return requests.filter(req => req.status === status);
}

export function filterByType(requests, type) {
    if (!type || type === 'all') return requests;
    return requests.filter(req => req.type === type);
}

export function sortRequests(requests, sortBy = 'request_id', order = 'asc') {
    return [...requests].sort((a, b) => {
        let aVal = a[sortBy];
        let bVal = b[sortBy];
        
        if (order === 'asc') {
            return aVal > bVal ? 1 : -1;
        } else {
            return aVal < bVal ? 1 : -1;
        }
    });
}
