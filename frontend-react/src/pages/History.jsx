import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { api } from '../services/api';
import './History.css';

function History() {
    const [files, setFiles] = useState([]);
    const [filteredFiles, setFilteredFiles] = useState([]);
    const [loading, setLoading] = useState(true);
    const [searchTerm, setSearchTerm] = useState('');

    useEffect(() => {
        loadHistory();
    }, []);

    useEffect(() => {
        if (searchTerm) {
            const filtered = files.filter((file) =>
                file.filename && file.filename.toLowerCase().includes(searchTerm.toLowerCase())
            );
            setFilteredFiles(filtered);
        } else {
            setFilteredFiles(files);
        }
    }, [searchTerm, files]);

    const loadHistory = async () => {
        try {
            const data = await api.getHistory(100);
            setFiles(data.files || []);
            setFilteredFiles(data.files || []);
            setLoading(false);
        } catch (error) {
            console.error('Error loading history:', error);
            setLoading(false);
        }
    };

    const formatSize = (chars) => {
        if (chars < 1000) return chars;
        if (chars < 1000000) return (chars / 1000).toFixed(1) + 'K';
        return (chars / 1000000).toFixed(1) + 'M';
    };

    if (loading) {
        return (
            <div className="container">
                <div className="card" style={{ textAlign: 'center', padding: '3rem' }}>
                    <div className="loading"></div>
                    <p style={{ marginTop: '1rem', color: 'var(--text-secondary)' }}>Loading history...</p>
                </div>
            </div>
        );
    }

    return (
        <div className="container">
            <div className="page-header">
                <h1 className="page-title">Upload History</h1>
                <p className="page-subtitle">View and manage previously generated test cases</p>
            </div>

            <div className="card" style={{ marginBottom: '2rem' }}>
                <div className="card-content">
                    <input
                        type="text"
                        placeholder="🔍 Search by filename..."
                        value={searchTerm}
                        onChange={(e) => setSearchTerm(e.target.value)}
                        className="search-input"
                    />
                </div>
            </div>

            {filteredFiles.length === 0 ? (
                <div className="card" style={{ textAlign: 'center', padding: '3rem' }}>
                    <p style={{ fontSize: '3rem', marginBottom: '1rem' }}>📂</p>
                    <h3 style={{ marginBottom: '0.5rem' }}>No Files Yet</h3>
                    <p style={{ color: 'var(--text-secondary)', marginBottom: '1.5rem' }}>
                        Upload your first PDF to get started!
                    </p>
                    <Link to="/upload" className="btn btn-primary">
                        Upload PDF
                    </Link>
                </div>
            ) : (
                filteredFiles.map((file) => (
                    <div key={file.file_id} className="history-item">
                        <Link to={`/testcases?id=${file.file_id}`} style={{ textDecoration: 'none', color: 'inherit' }}>
                            <div className="history-header">
                                <div>
                                    <div className="history-title">📄 {file.filename || 'Unknown File'}</div>
                                    <div className="history-date">
                                        {new Date(file.created_at).toLocaleString('en-US', {
                                            month: 'short',
                                            day: 'numeric',
                                            year: 'numeric',
                                            hour: '2-digit',
                                            minute: '2-digit',
                                        })}
                                    </div>
                                </div>
                                <span className={`badge ${file.status === 'success' ? 'badge-success' : 'badge-warning'}`}>
                                    {file.status === 'success' ? '✅ Success' : '⚠️ Partial'}
                                </span>
                            </div>

                            <div className="history-stats">
                                <div className="stat-item">
                                    <div className="stat-item-value">{file.pages || 0}</div>
                                    <div className="stat-item-label">Pages</div>
                                </div>
                                <div className="stat-item">
                                    <div className="stat-item-value">{formatSize(file.extracted_text_length || 0)}</div>
                                    <div className="stat-item-label">Text Length</div>
                                </div>
                                <div className="stat-item">
                                    <div className="stat-item-value">{file.model_used || 'AI'}</div>
                                    <div className="stat-item-label">Model</div>
                                </div>
                            </div>
                        </Link>

                        <div style={{ marginTop: '1rem', display: 'flex', gap: '0.5rem' }}>
                            <a
                                href={api.downloadPDF(file.file_id)}
                                onClick={(e) => e.stopPropagation()}
                                className="btn btn-secondary"
                                style={{ flex: 1, textAlign: 'center', textDecoration: 'none' }}
                                download
                            >
                                📥 PDF
                            </a>
                            <a
                                href={api.downloadJSON(file.file_id)}
                                onClick={(e) => e.stopPropagation()}
                                className="btn btn-secondary"
                                style={{ flex: 1, textAlign: 'center', textDecoration: 'none' }}
                                download
                            >
                                📥 JSON
                            </a>
                            <a
                                href={api.downloadMarkdown(file.file_id)}
                                onClick={(e) => e.stopPropagation()}
                                className="btn btn-secondary"
                                style={{ flex: 1, textAlign: 'center', textDecoration: 'none' }}
                                download
                            >
                                📥 Markdown
                            </a>
                        </div>
                    </div>
                ))
            )}
        </div>
    );
}

export default History;
