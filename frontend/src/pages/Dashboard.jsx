import React, { useState } from 'react';
import { sourcingService } from '../services/api';

const Dashboard = () => {
  const [image, setImage] = useState(null);
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);

  const handleSearch = async () => {
    setLoading(true);
    try {
      const data = await sourcingService.searchProducts(image);
      setResults(data.top_suppliers);
    } catch (e) {
      console.error("Search failed", e);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="p-8 bg-slate-50 min-h-screen">
      <h1 className="text-3xl font-bold mb-6 text-slate-800">B2B Wholesale Arbitrage</h1>
      
      <div className="bg-white p-6 rounded-xl shadow-sm mb-8 border border-slate-200">
        <label className="block text-sm font-medium text-slate-700 mb-2">Product Image URL or Upload</label>
        <div className="flex gap-4">
          <input 
            type="text" 
            className="flex-1 p-2 border rounded-lg outline-none focus:ring-2 ring-blue-500" 
            placeholder="https://..." 
            onChange={(e) => setImage(e.target.value)}
          />
          <button 
            onClick={handleSearch} 
            disabled={loading}
            className="bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700 disabled:bg-slate-400 transition-all"
          >
            {loading ? 'Searching...' : 'Find Sources'}
          </button>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {results.map((supplier, idx) => (
          <div key={idx} className="bg-white p-6 rounded-xl shadow-sm border border-slate-200 hover:border-blue-300 transition-all">
            <div className="flex justify-between items-start mb-4">
              <h3 className="font-bold text-lg text-slate-800">{supplier.name}</h3>
              <span className="bg-green-100 text-green-800 text-xs font-semibold px-2 py-1 rounded">Rating: {supplier.rating}</span>
            </div>
            <div className="text-sm text-slate-600 space-y-2">
              <p>Price: <span className="font-mono font-bold text-slate-900">${supplier.price}</span></p>
              <p>MOQ: <span className="font-bold text-slate-900">{supplier.moq} units</span></p>
              <p>Location: {supplier.location}</p>
            </div>
            <button className="w-full mt-6 py-2 bg-slate-800 text-white rounded-lg hover:bg-slate-900 transition-all text-sm font-medium">
              Start Negotiation
            </button>
          </div>
        ))}
      </div>
    </div>
  );
};

export default Dashboard;
