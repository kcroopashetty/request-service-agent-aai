// Statistics Calculator
export function calculateStats(requests) {
    const stats = {
        total: requests.length,
        byStatus: {},
        byType: {},
        pending: 0,
        approved: 0,
        rejected: 0
    };

    requests.forEach(req => {
        stats.byStatus[req.status] = (stats.byStatus[req.status] || 0) + 1;
        stats.byType[req.type] = (stats.byType[req.type] || 0) + 1;
        
        if (req.status === 'pending') stats.pending++;
        if (req.status === 'approved') stats.approved++;
        if (req.status === 'rejected') stats.rejected++;
    });

    return stats;
}
