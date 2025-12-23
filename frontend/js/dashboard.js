// Dashboard JavaScript
const API_BASE = 'http://127.0.0.1:8000';

// Load statistics on page load
document.addEventListener('DOMContentLoaded', async () => {
    await loadStatistics();
    await loadRecentActivity();
});

async function loadStatistics() {
    try {
        const response = await fetch(`${API_BASE}/history?limit=100`);
        const data = await response.json();
        
        document.getElementById('totalFiles').textContent = data.count || 0;
        
        // Calculate total pages
        let totalPages = 0;
        data.files.forEach(file => {
            totalPages += file.pages || 0;
        });
        document.getElementById('totalPages').textContent = totalPages;
        
        // Estimate test cases (approximate)
        const estimatedTestCases = data.count * 15; // Approximate 15 test cases per PDF
        document.getElementById('totalTestCases').textContent = estimatedTestCases;
        
    } catch (error) {
        console.error('Error loading statistics:', error);
        document.getElementById('totalFiles').textContent = '0';
        document.getElementById('totalTestCases').textContent = '0';
        document.getElementById('totalPages').textContent = '0';
    }
}

async function loadRecentActivity() {
    try {
        const response = await fetch(`${API_BASE}/history?limit=5`);
        const data = await response.json();
        
        const activityContainer = document.getElementById('recentActivity');
        
        if (data.count === 0) {
            activityContainer.innerHTML = `
                <p style="text-align: center; color: var(--text-secondary); padding: 2rem;">
                    No activity yet. Upload your first PDF to get started!
                </p>
            `;
            return;
        }
        
        activityContainer.innerHTML = data.files.map(file => `
            <div style="padding: 0.75rem; border-bottom: 1px solid var(--border-color); cursor: pointer;" 
                 onclick="window.location.href='testcases.html?id=${file.file_id}'">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <strong style="color: var(--text-primary);">${file.filename || 'Unknown'}</strong>
                        <p style="font-size: 0.875rem; color: var(--text-secondary); margin-top: 0.25rem;">
                            ${file.pages || 0} pages • ${file.status === 'success' ? '✅ Success' : '⚠️ Partial'}
                        </p>
                    </div>
                    <span class="badge badge-success">${new Date(file.created_at).toLocaleDateString()}</span>
                </div>
            </div>
        `).join('');
        
    } catch (error) {
        console.error('Error loading recent activity:', error);
        document.getElementById('recentActivity').innerHTML = `
            <p style="text-align: center; color: var(--error-red); padding: 2rem;">
                Failed to load recent activity
            </p>
        `;
    }
}

function refreshStats() {
    loadStatistics();
    loadRecentActivity();
}
