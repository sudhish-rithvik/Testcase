// History Page JavaScript
const API_BASE = 'http://127.0.0.1:8000';

let allFiles = [];

document.addEventListener('DOMContentLoaded', async () => {
    await loadHistory();

    // Search functionality
    document.getElementById('searchInput').addEventListener('input', (e) => {
        filterHistory(e.target.value);
    });
});

async function loadHistory() {
    try {
        const response = await fetch(`${API_BASE}/history?limit=100`);
        const data = await response.json();

        allFiles = data.files || [];
        displayHistory(allFiles);

    } catch (error) {
        console.error('Error loading history:', error);
        document.getElementById('historyContainer').innerHTML = `
            <div class="card" style="text-align: center; padding: 3rem;">
                <p style="font-size: 3rem; margin-bottom: 1rem;">❌</p>
                <h3 style="margin-bottom: 0.5rem;">Error Loading History</h3>
                <p style="color: var(--text-secondary);">${error.message}</p>
            </div>
        `;
    }
}

function displayHistory(files) {
    const container = document.getElementById('historyContainer');

    if (files.length === 0) {
        container.innerHTML = `
            <div class="card" style="text-align: center; padding: 3rem;">
                <p style="font-size: 3rem; margin-bottom: 1rem;">📂</p>
                <h3 style="margin-bottom: 0.5rem;">No Files Yet</h3>
                <p style="color: var(--text-secondary); margin-bottom: 1.5rem;">
                    Upload your first PDF to get started!
                </p>
                <a href="upload.html" class="btn btn-primary">Upload PDF</a>
            </div>
        `;
        return;
    }

    container.innerHTML = files.map(file => {
        const date = new Date(file.created_at);
        const formattedDate = date.toLocaleString('en-US', {
            month: 'short',
            day: 'numeric',
            year: 'numeric',
            hour: '2-digit',
            minute: '2-digit'
        });

        return `
            <div class="history-item" onclick="viewTestCases('${file.file_id}')">
                <div class="history-header">
                    <div>
                        <div class="history-title">📄 ${file.filename || 'Unknown File'}</div>
                        <div class="history-date">${formattedDate}</div>
                    </div>
                    <span class="badge ${file.status === 'success' ? 'badge-success' : 'badge-warning'}">
                        ${file.status === 'success' ? '✅ Success' : '⚠️ Partial'}
                    </span>
                </div>
                
                <div class="history-stats">
                    <div class="stat-item">
                        <div class="stat-item-value">${file.pages || 0}</div>
                        <div class="stat-item-label">Pages</div>
                    </div>
                    <div class="stat-item">
                        <div class="stat-item-value">${formatSize(file.extracted_text_length || 0)}</div>
                        <div class="stat-item-label">Text Length</div>
                    </div>
                    <div class="stat-item">
                        <div class="stat-item-value">${file.model_used || 'AI'}</div>
                        <div class="stat-item-label">Model</div>
                    </div>
                </div>
                
                <div style="margin-top: 1rem; display: flex; gap: 0.5rem;">
                    <button onclick="event.stopPropagation(); downloadFile('${file.file_id}', 'pdf')" class="btn btn-secondary" style="flex: 1;">
                        📥 PDF
                    </button>
                    <button onclick="event.stopPropagation(); downloadFile('${file.file_id}', 'json')" class="btn btn-secondary" style="flex: 1;">
                        📥 JSON
                    </button>
                    <button onclick="event.stopPropagation(); downloadFile('${file.file_id}', 'markdown')" class="btn btn-secondary" style="flex: 1;">
                        📥 Markdown
                    </button>
                </div>
            </div>
        `;
    }).join('');
}

function filterHistory(searchTerm) {
    const filtered = allFiles.filter(file =>
        file.filename && file.filename.toLowerCase().includes(searchTerm.toLowerCase())
    );
    displayHistory(filtered);
}

function formatSize(chars) {
    if (chars < 1000) return chars;
    if (chars < 1000000) return (chars / 1000).toFixed(1) + 'K';
    return (chars / 1000000).toFixed(1) + 'M';
}

function viewTestCases(fileId) {
    window.location.href = `testcases.html?id=${fileId}`;
}

function downloadFile(fileId, type) {
    const endpoints = {
        pdf: `/download/pdf/${fileId}`,
        json: `/download/testcases/${fileId}`,
        markdown: `/download/markdown/${fileId}`
    };

    window.location.href = `${API_BASE}${endpoints[type]}`;
}
