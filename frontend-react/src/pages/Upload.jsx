import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { api } from '../services/api';
import './Upload.css';

function Upload() {
    const [selectedFile, setSelectedFile] = useState(null);
    const [uploading, setUploading] = useState(false);
    const [progress, setProgress] = useState(0);
    const [statusText, setStatusText] = useState('');
    const [dragOver, setDragOver] = useState(false);
    const navigate = useNavigate();

    const handleFileSelect = (file) => {
        if (!file.name.endsWith('.pdf')) {
            alert('Please select a PDF file');
            return;
        }

        if (file.size > 10 * 1024 * 1024) {
            alert('File size exceeds 10MB limit');
            return;
        }

        setSelectedFile(file);
    };

    const handleDrop = (e) => {
        e.preventDefault();
        setDragOver(false);
        const files = e.dataTransfer.files;
        if (files.length > 0) {
            handleFileSelect(files[0]);
        }
    };

    const handleUpload = async () => {
        if (!selectedFile) return;

        setUploading(true);
        setProgress(10);
        setStatusText('Uploading PDF...');

        try {
            await new Promise((resolve) => setTimeout(resolve, 500));
            setProgress(40);
            setStatusText('Extracting text...');

            const data = await api.uploadPDF(selectedFile);

            setProgress(70);
            setStatusText('Generating test cases...');
            await new Promise((resolve) => setTimeout(resolve, 2000));

            setProgress(100);
            setStatusText('Complete!');

            setTimeout(() => {
                navigate(`/testcases?id=${data.file_id}`);
            }, 1000);
        } catch (error) {
            alert('Error: ' + error.message);
            setUploading(false);
            setProgress(0);
        }
    };

    const formatFileSize = (bytes) => {
        if (bytes < 1024) return bytes + ' B';
        if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(2) + ' KB';
        return (bytes / (1024 * 1024)).toFixed(2) + ' MB';
    };

    return (
        <div className="container">
            <div className="page-header">
                <h1 className="page-title">Upload Healthcare PDF</h1>
                <p className="page-subtitle">Upload a PDF to generate comprehensive test cases</p>
            </div>

            <div className="grid grid-2">
                {/* Upload Section */}
                <div className="card">
                    <div className="card-header">
                        <h2 className="card-title">Select PDF File</h2>
                    </div>
                    <div className="card-content">
                        <div
                            className={`upload-zone ${dragOver ? 'drag-over' : ''}`}
                            onDragOver={(e) => {
                                e.preventDefault();
                                setDragOver(true);
                            }}
                            onDragLeave={() => setDragOver(false)}
                            onDrop={handleDrop}
                            onClick={() => document.getElementById('fileInput').click()}
                        >
                            <div className="upload-icon">📄</div>
                            <h3 style={{ marginBottom: '0.5rem' }}>Drag & Drop PDF Here</h3>
                            <p style={{ color: 'var(--text-secondary)', marginBottom: '1rem' }}>or click to browse</p>
                            <button className="btn btn-primary">Choose File</button>
                            <p style={{ marginTop: '1rem', fontSize: '0.875rem', color: 'var(--text-secondary)' }}>
                                Maximum file size: 10MB
                            </p>
                        </div>
                        <input
                            type="file"
                            id="fileInput"
                            accept=".pdf"
                            style={{ display: 'none' }}
                            onChange={(e) => e.target.files.length > 0 && handleFileSelect(e.target.files[0])}
                        />

                        {selectedFile && (
                            <div
                                style={{
                                    marginTop: '1rem',
                                    padding: '1rem',
                                    background: 'var(--bg-primary)',
                                    borderRadius: 'var(--radius-md)',
                                }}
                            >
                                <p>
                                    <strong>Selected:</strong> {selectedFile.name}
                                </p>
                                <p>
                                    <strong>Size:</strong> {formatFileSize(selectedFile.size)}
                                </p>
                            </div>
                        )}

                        {selectedFile && !uploading && (
                            <button
                                onClick={handleUpload}
                                className="btn btn-success"
                                style={{ width: '100%', marginTop: '1rem', justifyContent: 'center' }}
                            >
                                🚀 Generate Test Cases
                            </button>
                        )}

                        {uploading && (
                            <div style={{ marginTop: '1rem' }}>
                                <p style={{ marginBottom: '0.5rem', fontWeight: 600 }}>{statusText}</p>
                                <div className="progress-bar">
                                    <div className="progress-fill" style={{ width: `${progress}%` }}></div>
                                </div>
                            </div>
                        )}
                    </div>
                </div>

                {/* Instructions */}
                <div className="card">
                    <div className="card-header">
                        <h2 className="card-title">Instructions</h2>
                    </div>
                    <div className="card-content">
                        <div style={{ display: 'flex', flexDirection: 'column', gap: '1.5rem' }}>
                            <div>
                                <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem', marginBottom: '0.5rem' }}>
                                    <div className="step-number">1</div>
                                    <h4>Upload PDF</h4>
                                </div>
                                <p className="instruction-text">
                                    Select a healthcare-related PDF document (requirements, user stories, etc.)
                                </p>
                            </div>

                            <div>
                                <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem', marginBottom: '0.5rem' }}>
                                    <div className="step-number" style={{ background: 'var(--secondary-teal)' }}>
                                        2
                                    </div>
                                    <h4>AI Processing</h4>
                                </div>
                                <p className="instruction-text">
                                    Our AI extracts text and generates comprehensive test cases focused on healthcare compliance
                                </p>
                            </div>

                            <div>
                                <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem', marginBottom: '0.5rem' }}>
                                    <div className="step-number" style={{ background: 'var(--success-green)' }}>
                                        3
                                    </div>
                                    <h4>Review & Download</h4>
                                </div>
                                <p className="instruction-text">
                                    View organized test cases and download in JSON or Markdown format
                                </p>
                            </div>

                            <div className="tip-box">
                                <strong style={{ color: 'var(--primary-blue)' }}>💡 Tip:</strong>
                                <p style={{ marginTop: '0.5rem', fontSize: '0.9rem' }}>
                                    PDFs with clear healthcare requirements generate better test cases. Include details about workflows,
                                    data, and compliance needs.
                                </p>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
}

export default Upload;
