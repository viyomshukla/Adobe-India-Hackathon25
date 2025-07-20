import React, { useState } from 'react';
import axios from 'axios';
import './App.css';

function App() {
  const [inputJson, setInputJson] = useState(null);
  const [pdfs, setPdfs] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [downloadUrl, setDownloadUrl] = useState('');

  const handleInputJsonChange = (e) => {
    setInputJson(e.target.files[0]);
    setError('');
    setDownloadUrl('');
  };

  const handlePdfsChange = (e) => {
    setPdfs(Array.from(e.target.files));
    setError('');
    setDownloadUrl('');
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setDownloadUrl('');
    if (!inputJson) {
      setError('Please upload input.json');
      return;
    }
    if (pdfs.length === 0) {
      setError('Please upload at least one PDF');
      return;
    }
    setLoading(true);
    try {
      const formData = new FormData();
      formData.append('input_json', inputJson);
      pdfs.forEach((pdf) => formData.append('pdfs', pdf));
      const response = await axios.post('http://localhost:8000/analyze/', formData, {
        responseType: 'blob',
        headers: { 'Content-Type': 'multipart/form-data' },
      });
      // Create a download link
      const url = window.URL.createObjectURL(new Blob([response.data]));
      setDownloadUrl(url);
    } catch (err) {
      setError('Error processing files. Please check your input and try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <>
      <div className="app-header">Persona-Driven Document Intelligence</div>
      <div className="container">
        <h2 className="title">Upload & Analyze</h2>
        <form onSubmit={handleSubmit} className="form">
          <div className="form-group">
            <label><b>input.json</b>:</label><br />
            <input type="file" accept="application/json" onChange={handleInputJsonChange} className="file-input" />
          </div>
          <div className="form-group">
            <label><b>PDFs</b>:</label><br />
            <input type="file" accept="application/pdf" multiple onChange={handlePdfsChange} className="file-input" />
          </div>
          <button type="submit" disabled={loading} className="analyze-btn">
            {loading ? 'Processing...' : 'Analyze'}
          </button>
        </form>
        {error && <div className="error-msg">{error}</div>}
        {downloadUrl && (
          <div className="download-section">
            <a href={downloadUrl} download="challenge1b_output.json" className="download-link">
              Download challenge1b_output.json
            </a>
          </div>
        )}
        <div className="instructions">
          <div>1. Upload your <b>input.json</b> and all required PDFs.</div>
          <div>2. Click <b>Analyze</b> to process.</div>
          <div>3. Download the output JSON.</div>
        </div>
      </div>
    </>
  );
}

export default App; 