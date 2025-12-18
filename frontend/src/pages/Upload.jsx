import React from 'react';
import { useNavigate } from 'react-router-dom';
import FileUploader from '../components/FileUploader';
import api from '../services/api';

const Upload = () => {
  const navigate = useNavigate();

  const handleUploadSuccess = async () => {
    // After upload, trigger KYC start
    try {
      const response = await api.post('/kyc/start');
      // Redirect to review page with KYC ID
      navigate(`/review/${response.data.id}`);
    } catch (error) {
      console.error("Failed to start KYC", error);
      alert("Failed to start KYC process");
    }
  };

  return (
    <div className="p-8 max-w-2xl mx-auto">
      <h1 className="text-2xl font-bold mb-6">Upload Documents</h1>
      <p className="mb-6 text-gray-600">Please upload your Aadhaar and PAN card to proceed.</p>
      <FileUploader onUploadSuccess={handleUploadSuccess} />
    </div>
  );
};

export default Upload;
