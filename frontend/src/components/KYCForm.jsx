import React, { useState, useEffect } from 'react';

const KYCForm = ({ initialData, onConfirm }) => {
  const [formData, setFormData] = useState(initialData || {});

  useEffect(() => {
    if (initialData) {
      setFormData(initialData);
    }
  }, [initialData]);

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    onConfirm(formData);
  };

  return (
    <form onSubmit={handleSubmit} className="p-4 border rounded shadow-md bg-white">
      <h3 className="text-lg font-bold mb-4">Review KYC Data</h3>
      <div className="grid grid-cols-1 gap-4">
        {Object.keys(formData).map((key) => (
          <div key={key}>
            <label className="block text-sm font-medium text-gray-700 capitalize">{key.replace('_', ' ')}</label>
            <input
              type="text"
              name={key}
              value={formData[key] || ''}
              onChange={handleChange}
              className="mt-1 block w-full border-gray-300 rounded-md shadow-sm p-2 border"
            />
          </div>
        ))}
      </div>
      <div className="mt-6">
        <button type="submit" className="w-full bg-green-600 text-white py-2 px-4 rounded hover:bg-green-700">
          Confirm & Submit
        </button>
      </div>
    </form>
  );
};

export default KYCForm;
