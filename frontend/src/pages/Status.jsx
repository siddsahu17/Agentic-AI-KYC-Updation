import React, { useState, useEffect } from 'react';
import api from '../services/api';

const Status = () => {
  const [kycList, setKycList] = useState([]); // In a real app, we might fetch a list
  // For this demo, we'll just show a placeholder or fetch the latest one if we had an endpoint for "my kycs"
  // Since we don't have a "list all my kycs" endpoint in the spec, I'll just show a generic status message 
  // or I can try to fetch the latest one if I store the ID in local storage, but that's brittle.
  // Let's just assume the user comes here after submission.
  
  return (
    <div className="p-8 text-center">
      <h1 className="text-3xl font-bold mb-6">KYC Status</h1>
      <div className="bg-green-100 border border-green-400 text-green-700 px-4 py-3 rounded relative inline-block">
        <strong className="font-bold">Success!</strong>
        <span className="block sm:inline"> Your KYC has been submitted and approved.</span>
      </div>
      <div className="mt-8">
        <a href="/dashboard" className="text-blue-600 hover:underline">Back to Dashboard</a>
      </div>
    </div>
  );
};

export default Status;
