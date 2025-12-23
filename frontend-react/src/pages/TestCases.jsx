import { useState, useEffect } from 'react';
import { useSearchParams } from 'react-router-dom';
import { api } from '../services/api';
import './TestCases.css';

function TestCases() {
    const [searchParams] = useSearchParams();
    const fileId = searchParams.get('id');
    const [data, setData] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        if (fileId) {
            loadTestCases();
        }
    }, [fileId]);

    const loadTestCases = async () => {
        try {
            const result = await api.getFile(fileId);
            setData(result);
            setLoading(false);
        } catch (err) {
            setError(err.message);
            setLoading(false);
        }
    };

    const displayTestCases = (text) => {
        if (!text || text === 'No test cases available') {
            return <div className="no-testcases">No test cases available</div>;
        }

        // Simple markdown-like rendering
        return (
            <div className="testcase-content">
                {text.split('\n').map((line, index) => {
                    // Headers
                    if (line.startsWith('###')) {
                        return (
                            <h3 key={index} className="testcase-section-title">
                                {line.replace(/###/g, '').trim()}
                            </h3>
                        );
                    }
                    if (line.startsWith('##')) {
                        return (
                            <h2 key={index} className="testcase-main-title">
                                {line.replace(/##/g, '').trim()}
                            </h2>
                        );
                    }
                    if (line.startsWith('#')) {
                        return (
                            <h1 key={index} className="testcase-title">
                                {line.replace(/#/g, '').trim()}
                            </h1>
                        );
                    }
                    // Bold text
                    if (line.includes('**')) {
                        const parts = line.split('**');
                        return (
                            <p key={index}>
                                {parts.map((part, i) => (i % 2 === 1 ? <strong key={i}>{part}</strong> : part))}
                            </p>
                        );
                    }
                    // List items
                    if (line.trim().startsWith('-')) {
                        return (
                            <li key={index} className="testcase-list-item">
                                {line.trim().substring(1).trim()}
                            </li>
                        );
                    }
                    // Regular text
                    if (line.trim()) {
                        return (
                            <p key={index} className="testcase-text">
                                {line}
                            </p>
                        );
                    }
                    return <br key={index} />;
                })}
            </div>
        );
    };

    if (loading) {
        return (
            <div className="container">
                <div className="card" style={{ textAlign: 'center', padding: '3rem' }}>
                    <div className="loading"></div>
                    <p style={{ marginTop: '1rem' }}>Loading test cases...</p>
                </div>
            </div>
        );
    }

    if (error) {
        return (
            <div className="container">
                <div className="card" style={{ textAlign: 'center', padding: '3rem' }}>
                    <p style={{ fontSize: '3rem', marginBottom: '1rem' }}>❌</p>
                    <h3 style={{ marginBottom: '0.5rem' }}>Error Loading Test Cases</h3>
                    <p style={{ color: 'var(--text-secondary)' }}>{error}</p>
                </div>
            </div>
        );
    }

    return (
        <div className="container">
            <div className="page-header" style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                <div>
                    <h1 className="page-title">Test Cases</h1>
                    <p className="page-subtitle">File: {data?.filename || 'Unknown'}</p>
                </div>
                <div style={{ display: 'flex', gap: '1rem' }}>
                    <a href={api.downloadJSON(fileId)} className="btn btn-primary" download>
                        📥 Download JSON
                    </a>
                    <a href={api.downloadMarkdown(fileId)} className="btn btn-secondary" download>
                        📝 Download Markdown
                    </a>
                </div>
            </div>

            <div className="card">
                <div className="card-content">{displayTestCases(data?.test_cases)}</div>
            </div>
        </div>
    );
}

export default TestCases;
