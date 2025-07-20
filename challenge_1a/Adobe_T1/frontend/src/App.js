import React, { useState, useRef } from 'react';

function Spinner() {
  return (
    <div style={{ textAlign: 'center', margin: '2rem 0' }}>
      <div style={{
        display: 'inline-block',
        width: 40,
        height: 40,
        border: '4px solid #1976d2',
        borderTop: '4px solid #fff',
        borderRadius: '50%',
        animation: 'spin 1s linear infinite',
      }} />
      <style>{`
        @keyframes spin {
          0% { transform: rotate(0deg); }
          100% { transform: rotate(360deg); }
        }
      `}</style>
    </div>
  );
}

function App() {
  const [files, setFiles] = useState([]);
  const [results, setResults] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const fileInputRef = useRef();

  const handleFileChange = (e) => {
    setFiles(e.target.files);
    setResults(null);
    setError(null);
  };

  const handleChooseFiles = () => {
    fileInputRef.current.click();
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!files.length) return;
    setLoading(true);
    setError(null);
    setResults(null);
    const formData = new FormData();
    for (let i = 0; i < files.length; i++) {
      formData.append('files', files[i]);
    }
    try {
      const res = await fetch('http://localhost:5000/extract-outline', {
        method: 'POST',
        body: formData,
      });
      if (!res.ok) throw new Error('Failed to extract outline');
      const data = await res.json();
      setResults(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ minHeight: '100vh', background: '#f4f6fa' }}>
      {/* Header */}
      <header style={{ background: '#1976d2', color: '#fff', padding: '1.5rem 0', textAlign: 'center', boxShadow: '0 2px 8px #0001' }}>
        <h1 style={{ margin: 0, fontWeight: 700, letterSpacing: 1 }}>PDF Outline Extractor</h1>
        <p style={{ margin: 0, fontWeight: 300 }}>Upload your PDF(s) and get a structured outline instantly</p>
      </header>

      {/* Main Content */}
      <main style={{ maxWidth: 800, margin: '2rem auto', background: '#fff', borderRadius: 12, boxShadow: '0 2px 16px #0002', padding: '2rem' }}>
        <form onSubmit={handleSubmit} style={{ display: 'flex', flexWrap: 'wrap', alignItems: 'center', gap: 16, marginBottom: 24 }}>
          {/* Hidden file input */}
          <input
            type="file"
            accept="application/pdf"
            multiple
            onChange={handleFileChange}
            ref={fileInputRef}
            style={{ display: 'none' }}
          />
          {/* Custom choose file button */}
          <button
            type="button"
            onClick={handleChooseFiles}
            style={{
              background: '#fff',
              color: '#1976d2',
              border: '2px solid #1976d2',
              borderRadius: 6,
              padding: '0.7rem 1.5rem',
              fontWeight: 600,
              cursor: loading ? 'not-allowed' : 'pointer',
              fontSize: 16,
              boxShadow: '0 1px 4px #0001',
              transition: 'background 0.2s, color 0.2s',
              outline: 'none',
            }}
            disabled={loading}
            aria-label="Choose PDF files"
          >
            {files.length ? 'Change Files' : 'Choose PDF Files'}
          </button>
          {/* Show selected file names */}
          <div style={{ flex: 1, minWidth: 0, color: '#333', fontSize: 15, overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>
            {files.length
              ? Array.from(files).map(f => f.name).join(', ')
              : <span style={{ color: '#888' }}>No files selected</span>}
          </div>
          <button
            type="submit"
            disabled={loading || !files.length}
            style={{
              background: '#1976d2', color: '#fff', border: 'none', borderRadius: 6, padding: '0.7rem 1.5rem', fontWeight: 600, cursor: loading || !files.length ? 'not-allowed' : 'pointer', fontSize: 16, boxShadow: '0 1px 4px #0001', transition: 'background 0.2s',
            }}
          >
            {loading ? 'Processing...' : 'Extract Outline'}
          </button>
        </form>
        {error && <div style={{ color: '#d32f2f', background: '#fff0f0', border: '1px solid #fbb', borderRadius: 6, padding: 12, marginBottom: 20 }}>{error}</div>}
        {loading && <Spinner />}
        {results && (
          <div style={{ marginTop: 10 }}>
            <h2 style={{ color: '#1976d2', fontWeight: 600, marginBottom: 24 }}>Results</h2>
            <div style={{ display: 'flex', flexDirection: 'column', gap: 24 }}>
              {Object.entries(results).map(([filename, outline]) => (
                <div key={filename} style={{ background: '#f9fbff', border: '1px solid #e3eaf5', borderRadius: 10, padding: 20, boxShadow: '0 1px 6px #0001' }}>
                  <h3 style={{ color: '#1976d2', margin: 0 }}>{filename}</h3>
                  <div style={{ margin: '8px 0 0 0' }}><strong>Title:</strong> {outline.title}</div>
                  <div style={{ marginTop: 10 }}>
                    <strong>Outline:</strong>
                    {outline.outline.length === 0 ? (
                      <div style={{ color: '#888', marginTop: 6 }}>No headings detected.</div>
                    ) : (
                      <ul style={{ margin: '8px 0 0 0', paddingLeft: 20 }}>
                        {outline.outline.map((item, idx) => (
                          <li key={idx} style={{ marginBottom: 4 }}>
                            <span style={{
                              fontWeight: item.level === 'H1' ? 700 : item.level === 'H2' ? 600 : 500,
                              color: item.level === 'H1' ? '#1976d2' : item.level === 'H2' ? '#388e3c' : '#6d4c41',
                            }}>
                              [{item.level}] {item.text}
                            </span>
                            {` (Page ${item.page})`}
                          </li>
                        ))}
                      </ul>
                    )}
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}
      </main>

      {/* Footer */}
      <footer style={{ textAlign: 'center', color: '#888', fontSize: 15, margin: '2rem 0 1rem 0' }}>
        &copy; {new Date().getFullYear()} PDF Outline Extractor &mdash; Powered by React & Flask
      </footer>
    </div>
  );
}

export default App; 