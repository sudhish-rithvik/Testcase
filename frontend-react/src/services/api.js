// API Service for backend communication
const API_BASE = 'http://127.0.0.1:8000';

export const api = {
    // Get upload history
    getHistory: async (limit = 100) => {
        const response = await fetch(`${API_BASE}/history?limit=${limit}`);
        return response.json();
    },

    // Get file metadata
    getFile: async (fileId) => {
        const response = await fetch(`${API_BASE}/file/${fileId}`);
        return response.json();
    },

    // Upload PDF
    uploadPDF: async (file, onProgress) => {
        const formData = new FormData();
        formData.append('file', file);

        const response = await fetch(`${API_BASE}/upload-pdf`, {
            method: 'POST',
            body: formData,
        });

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'Upload failed');
        }

        return response.json();
    },

    // Delete file
    deleteFile: async (fileId) => {
        const response = await fetch(`${API_BASE}/file/${fileId}`, {
            method: 'DELETE',
        });

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'Delete failed');
        }

        return response.json();
    },

    // Download URLs
    downloadJSON: (fileId) => `${API_BASE}/download/testcases/${fileId}`,
    downloadMarkdown: (fileId) => `${API_BASE}/download/markdown/${fileId}`,
    downloadPDF: (fileId) => `${API_BASE}/download/pdf/${fileId}`,
};
