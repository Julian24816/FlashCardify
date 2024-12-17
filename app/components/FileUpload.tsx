'use client'

import { useState } from 'react';
import axios from 'axios';

export default function FileUpload() {
  const [file, setFile] = useState(null);
  const [responseText, setResponseText] = useState('');
  const [error, setError] = useState('');

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const handleUpload = async () => {
    if (!file) {
      alert('Please select a file');
      return;
    }

    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await axios.post('/api/upload', formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
      });
      setResponseText(response.data.text);
      setError('');
    } catch (err) {
      setError(err.response?.data?.error || 'An error occurred');
      setResponseText('');
    }
  };

  return (
    <div style={{ padding: '20px', textAlign: 'center' }}>
      <h1>Upload Notes</h1>
      <input type="file" onChange={handleFileChange} />
      <button onClick={handleUpload} style={{ marginLeft: '10px' }}>
        Upload
      </button>
      {responseText && (
        <div>
          <h2>Extracted Text:</h2>
          <pre>{responseText}</pre>
        </div>
      )}
      {error && (
        <div>
          <h2 style={{ color: 'red' }}>Error:</h2>
          <p>{error}</p>
        </div>
      )}
    </div>
  );
}
