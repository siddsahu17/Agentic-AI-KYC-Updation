import React, { useState } from 'react';
import api from '../services/api';

const FileUploader = ({ onUploadSuccess }) => {
  const [file, setFile] = useState(null);
  const [docType, setDocType] = useState('aadhaar');
  const [uploading, setUploading] = useState(false);

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const handleUpload = async () => {
    if (!file) return;
    setUploading(true);
    const formData = new FormData();
    formData.append('file', file);
    
    try {
      await api.post(`/upload/document?doc_type=${docType}`, formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      onUploadSuccess();
      setFile(null);
    } catch (error) {
      console.error("Upload failed", error);
      alert("Upload failed");
    } finally {
      setUploading(false);
    }
  };

  return (
    <div className="p-4 border rounded shadow-md bg-white">
      <h3 className="text-lg font-bold mb-4">Upload Document</h3>
      <div className="mb-4">
        <label className="block text-sm font-medium text-gray-700">Document Type</label>
        <select 
          value={docType} 
          onChange={(e) => setDocType(e.target.value)}
          className="mt-1 block w-full border-gray-300 rounded-md shadow-sm p-2 border"
        >
          <option value="aadhaar">Aadhaar</option>
          <option value="pan">PAN Card</option>
        </select>
      </div>
      <div className="mb-4">
        <input type="file" onChange={handleFileChange} className="block w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-blue-50 file:text-blue-700 hover:file:bg-blue-100"/>
      </div>
      <button 
        onClick={handleUpload} 
        disabled={!file || uploading}
        className="w-full bg-blue-600 text-white py-2 px-4 rounded hover:bg-blue-700 disabled:bg-gray-400"
      >
        {uploading ? 'Uploading...' : 'Upload'}
      </button>
    </div>
  );
};

export default FileUploader;
