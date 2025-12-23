// Upload Page JavaScript
const API_BASE = 'http://127.0.0.1:8000';

const uploadZone = document.getElementById('uploadZone');
const fileInput = document.getElementById('fileInput');
const fileInfo = document.getElementById('fileInfo');
const uploadButton = document.getElementById('uploadButton');
const progressSection = document.getElementById('progressSection');

let selectedFile = null;

// Click to select file
uploadZone.addEventListener('click', () => fileInput.click());

// Drag and drop handlers
uploadZone.addEventListener('dragover', (e) => {
    e.preventDefault();
    uploadZone.classList.add('drag-over');
});

uploadZone.addEventListener('dragleave', () => {
    uploadZone.classList.remove('drag-over');
});

uploadZone.addEventListener('drop', (e) => {
    e.preventDefault();
    uploadZone.classList.remove('drag-over');
    const files = e.dataTransfer.files;
    if (files.length > 0) {
        handleFileSelection(files[0]);
    }
});

// File input change
fileInput.addEventListener('change', (e) => {
    if (e.target.files.length > 0) {
        handleFileSelection(e.target.files[0]);
    }
});

function handleFileSelection(file) {
    if (!file.name.endsWith('.pdf')) {
        alert('Please select a PDF file');
        return;
    }

    if (file.size > 10 * 1024 * 1024) {
        alert('File size exceeds 10MB limit');
        return;
    }

    selectedFile = file;
    document.getElementById('fileName').textContent = file.name;
    document.getElementById('fileSize').textContent = formatFileSize(file.size);
    fileInfo.classList.remove('hidden');
    uploadButton.style.display = 'flex';
}

function formatFileSize(bytes) {
    if (bytes < 1024) return bytes + ' B';
    if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(2) + ' KB';
    return (bytes / (1024 * 1024)).toFixed(2) + ' MB';
}

// Upload button click
uploadButton.addEventListener('click', async () => {
    if (!selectedFile) return;

    uploadButton.disabled = true;
    progressSection.classList.remove('hidden');

    const formData = new FormData();
    formData.append('file', selectedFile);

    try {
        updateProgress(10, 'Uploading PDF...');

        const response = await fetch(`${API_BASE}/upload-pdf`, {
            method: 'POST',
            body: formData
        });

        updateProgress(40, 'Extracting text...');

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.detail || 'Upload failed');
        }

        updateProgress(70, 'Generating test cases...');

        // Simulate processing time
        await new Promise(resolve => setTimeout(resolve, 2000));

        updateProgress(100, 'Complete!');

        // Redirect to test cases page
        setTimeout(() => {
            window.location.href = `testcases.html?id=${data.file_id}`;
        }, 1000);

    } catch (error) {
        alert('Error: ' + error.message);
        uploadButton.disabled = false;
        progressSection.classList.add('hidden');
    }
});

function updateProgress(percent, text) {
    document.getElementById('progressFill').style.width = percent + '%';
    document.getElementById('statusText').textContent = text;
}
