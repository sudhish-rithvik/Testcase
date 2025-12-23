// Test Cases Page JavaScript
const API_BASE = 'http://127.0.0.1:8000';

let currentFileId = null;
let currentData = null;

document.addEventListener('DOMContentLoaded', async () => {
    const urlParams = new URLSearchParams(window.location.search);
    currentFileId = urlParams.get('id');

    if (currentFileId) {
        await loadTestCases(currentFileId);
    }
});

async function loadTestCases(fileId) {
    try {
        const response = await fetch(`${API_BASE}/file/${fileId}`);
        const data = await response.json();

        currentData = data;

        document.getElementById('docTitle').textContent = `File: ${data.filename || 'Unknown'}`;

        // Parse test cases text into structured format
        const testCasesText = data.test_cases || 'No test cases available';

        displayTestCases(testCasesText);

    } catch (error) {
        console.error('Error loading test cases:', error);
        document.getElementById('testCasesContainer').innerHTML = `
            <div class="card" style="text-align: center; padding: 3rem;">
                <p style="font-size: 3rem; margin-bottom: 1rem;">❌</p>
                <h3 style="margin-bottom: 0.5rem;">Error Loading Test Cases</h3>
                <p style="color: var(--text-secondary);">${error.message}</p>
            </div>
        `;
    }
}

function displayTestCases(text) {
    const container = document.getElementById('testCasesContainer');

    // Split by test case patterns (TC-001, TC-002, etc.)
    const sections = text.split(/(?=###\s+TC-)/);

    if (sections.length === 1) {
        // No structured test cases, display as markdown
        container.innerHTML = `
            <div class="card">
                <div class="card-content" style="white-space: pre-wrap; font-family: monospace;">
                    ${escapeHtml(text)}
                </div>
            </div>
        `;
        return;
    }

    container.innerHTML = sections.map((section, index) => {
        if (index === 0 && !section.includes('TC-')) {
            // Header section
            return `
                <div class="card" style="margin-bottom: 2rem;">
                    <div class="card-content" style="white-space: pre-wrap;">
                        ${convertMarkdownToHtml(section)}
                    </div>
                </div>
            `;
        }

        // Extract test case details
        const idMatch = section.match(/TC-(\d+)/);
        const titleMatch = section.match(/###\s+TC-\d+:\s+(.+)/);

        return `
            <div class="testcase-box">
                <span class="testcase-id">TC-${idMatch ? idMatch[1] : index}</span>
                <h3 class="testcase-title">${titleMatch ? titleMatch[1] : 'Test Case'}</h3>
                <div class="testcase-content" style="white-space: pre-wrap;">
                    ${convertMarkdownToHtml(section.replace(/###\s+TC-\d+:.+\n/, ''))}
                </div>
            </div>
        `;
    }).join('');
}

function convertMarkdownToHtml(text) {
    return text
        .replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>')
        .replace(/\*(.+?)\*/g, '<em>$1</em>')
        .replace(/`(.+?)`/g, '<code style="background: var(--bg-primary); padding: 0.125rem 0.375rem; border-radius: 0.25rem;">$1</code>')
        .replace(/^- (.+)$/gm, '<li>$1</li>');
}

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

async function downloadJSON() {
    if (!currentFileId) return;
    window.location.href = `${API_BASE}/download/testcases/${currentFileId}`;
}

async function downloadMarkdown() {
    if (!currentFileId) return;
    window.location.href = `${API_BASE}/download/markdown/${currentFileId}`;
}
