import React from 'react';
import { Link } from 'react-router-dom';

const Dashboard = () => {
  return (
    <div className="p-8">
      <h1 className="text-3xl font-bold mb-8">KYC Dashboard</h1>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div className="bg-white p-6 rounded shadow hover:shadow-lg transition">
          <h2 className="text-xl font-bold mb-2">New KYC</h2>
          <p className="text-gray-600 mb-4">Start a new KYC verification process.</p>
          <Link to="/upload" className="inline-block bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700">
            Start KYC
          </Link>
        </div>
        <div className="bg-white p-6 rounded shadow hover:shadow-lg transition">
          <h2 className="text-xl font-bold mb-2">Check Status</h2>
          <p className="text-gray-600 mb-4">View the status of your existing KYC.</p>
          <Link to="/status" className="inline-block bg-gray-600 text-white px-4 py-2 rounded hover:bg-gray-700">
            View Status
          </Link>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
