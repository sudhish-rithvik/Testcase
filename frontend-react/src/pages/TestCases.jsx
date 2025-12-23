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
            console.log('API Response:', result);

            // If test_cases field doesn't exist, try to fetch from S3 markdown URL
            if (!result.test_cases && result.testcases_md_url) {
                console.log('test_cases not in metadata, fetching from S3...');
                try {
                    const mdUrl = result.testcases_md_url.replace('s3://', 'https://s3.amazonaws.com/');
                    const mdResponse = await fetch(mdUrl);
                    if (mdResponse.ok) {
                        result.test_cases = await mdResponse.text();
                        console.log('Fetched test cases from S3:', result.test_cases.substring(0, 200));
                    }
                } catch (err) {
                    console.error('Failed to fetch from S3:', err);
                }
            }

            setData(result);
            setLoading(false);
        } catch (err) {
            setError(err.message);
            setLoading(false);
        }
    };

    const parseTestCases = (text) => {
        if (!text || text === 'No test cases available') {
            return [];
        }

        const testCases = [];
        // Split by test case markers (### TC-)
        const sections = text.split(/###\s+(TC-\d+)/);

        for (let i = 1; i < sections.length; i += 2) {
            const tcId = sections[i]; // TC-001, TC-002, etc.
            const content = sections[i + 1];

            if (!content) continue;

            // Extract title (first line after TC-ID)
            const lines = content.trim().split('\n');
            const title = lines[0].replace(/[*:]/g, '').trim();

            // Extract priority if exists
            const priorityMatch = content.match(/\*\*Priority\*\*:\s*([^\n]+)/i);
            const priority = priorityMatch ? priorityMatch[1].trim() : 'P2-Medium';

            // Extract type if exists
            const typeMatch = content.match(/\*\*Type\*\*:\s*([^\n]+)/i);
            const type = typeMatch ? typeMatch[1].trim() : 'Functional Test';

            testCases.push({
                id: tcId,
                title,
                priority,
                type,
                content: content.trim()
            });
        }

        return testCases;
    };

    const getPriorityColor = (priority) => {
        if (priority.includes('P0') || priority.includes('Critical')) return '#ef4444';
        if (priority.includes('P1') || priority.includes('High')) return '#f97316';
        if (priority.includes('P2') || priority.includes('Medium')) return '#3b82f6';
        return '#6b7280';
    };

    const renderTestCaseContent = (content) => {
        return content.split('\n').map((line, index) => {
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
        });
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

    const testCases = parseTestCases(data?.test_cases);

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

            {testCases.length === 0 ? (
                <div className="card">
                    <div className="card-content">
                        <div className="no-testcases">No test cases available</div>
                    </div>
                </div>
            ) : (
                <div className="testcases-grid">
                    {testCases.map((tc) => (
                        <div key={tc.id} className="testcase-card">
                            <div className="testcase-card-header">
                                <div>
                                    <span className="testcase-id">{tc.id}</span>
                                    <h3 className="testcase-title-text">{tc.title}</h3>
                                </div>
                                <div style={{ display: 'flex', gap: '0.5rem', flexWrap: 'wrap' }}>
                                    <span
                                        className="badge priority-badge"
                                        style={{ backgroundColor: getPriorityColor(tc.priority) }}
                                    >
                                        {tc.priority}
                                    </span>
                                    <span className="badge type-badge">
                                        {tc.type}
                                    </span>
                                </div>
                            </div>
                            <div className="testcase-card-content">
                                {renderTestCaseContent(tc.content)}
                            </div>
                        </div>
                    ))}
                </div>
            )}
        </div>
    );
}

export default TestCases;
