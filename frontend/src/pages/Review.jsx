import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import api from '../services/api';
import KYCForm from '../components/KYCForm';

const Review = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const [kycData, setKycData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchKYC = async () => {
      try {
        const response = await api.get(`/kyc/${id}`);
        setKycData(response.data);
      } catch (error) {
        console.error("Failed to fetch KYC data", error);
      } finally {
        setLoading(false);
      }
    };
    fetchKYC();
  }, [id]);

  const handleConfirm = async (updatedData) => {
    try {
      await api.post('/kyc/confirm', { extracted_data: updatedData });
      navigate('/status');
    } catch (error) {
      console.error("Failed to confirm KYC", error);
      alert("Failed to confirm KYC");
    }
  };

  if (loading) return <div className="p-8 text-center">Loading...</div>;
  if (!kycData) return <div className="p-8 text-center">KYC Record not found</div>;

  return (
    <div className="p-8 max-w-2xl mx-auto">
      <h1 className="text-2xl font-bold mb-6">Review & Confirm</h1>
      <p className="mb-6 text-gray-600">Please review the extracted data and correct any errors.</p>
      
      {kycData.status === 'processing' ? (
        <div className="text-center py-10">
          <p className="text-xl animate-pulse">Processing your documents...</p>
          <p className="text-sm text-gray-500 mt-2">This may take a few seconds.</p>
        </div>
      ) : (
        <KYCForm initialData={kycData.extracted_data} onConfirm={handleConfirm} />
      )}
    </div>
  );
};

export default Review;
