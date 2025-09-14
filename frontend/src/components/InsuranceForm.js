import React, { useState } from 'react';
import axios from 'axios';
import { Calculator, Loader, CheckCircle, AlertCircle, X } from 'lucide-react';

const InsuranceForm = () => {
  const [formData, setFormData] = useState({
    age: 29,
    sex: 'male',
    bmi: 26.5,
    children: 1,
    smoker: 'no',
    region: 'southeast'
  });

  const [prediction, setPrediction] = useState(null);
  const [recommendations, setRecommendations] = useState(null);
  const [loading, setLoading] = useState(false);
  const [recommendationsLoading, setRecommendationsLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleInputChange = (e) => {
    const { name, value, type } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: type === 'number' ? parseFloat(value) || 0 : value
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    setPrediction(null);
    setRecommendations(null);

    try {
      const response = await axios.post('http://localhost:8000/predict-insurance', formData);
      setPrediction(response.data);
    } catch (err) {
      setError(err.response?.data?.detail || 'An error occurred while predicting insurance cost');
    } finally {
      setLoading(false);
    }
  };

  const handleGetRecommendations = async () => {
    if (!prediction) return;
    
    setRecommendationsLoading(true);
    setError(null);

    try {
      const response = await axios.post('http://localhost:8000/get-recommendations', {
        price: prediction.estimated_price
      });
      setRecommendations(response.data.recommendations);
    } catch (err) {
      setError(err.response?.data?.detail || 'An error occurred while getting recommendations');
    } finally {
      setRecommendationsLoading(false);
    }
  };

  const handleCloseRecommendations = () => {
    setRecommendations(null);
  };

  return (
    <div className="space-y-6">
      <form onSubmit={handleSubmit} className="space-y-6">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {/* Age */}
          <div>
            <label htmlFor="age" className="block text-sm font-medium text-gray-700 mb-2">
              Age
            </label>
            <input
              type="number"
              id="age"
              name="age"
              value={formData.age}
              onChange={handleInputChange}
              min="0"
              max="100"
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
              required
            />
          </div>

          {/* Sex */}
          <div>
            <label htmlFor="sex" className="block text-sm font-medium text-gray-700 mb-2">
              Gender
            </label>
            <select
              id="sex"
              name="sex"
              value={formData.sex}
              onChange={handleInputChange}
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
            >
              <option value="male">Male</option>
              <option value="female">Female</option>
            </select>
          </div>

          {/* BMI */}
          <div>
            <label htmlFor="bmi" className="block text-sm font-medium text-gray-700 mb-2">
              BMI (Body Mass Index)
            </label>
            <input
              type="number"
              id="bmi"
              name="bmi"
              value={formData.bmi}
              onChange={handleInputChange}
              min="10"
              max="50"
              step="0.1"
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
              required
            />
          </div>

          {/* Children */}
          <div>
            <label htmlFor="children" className="block text-sm font-medium text-gray-700 mb-2">
              Number of Children
            </label>
            <input
              type="number"
              id="children"
              name="children"
              value={formData.children}
              onChange={handleInputChange}
              min="0"
              max="10"
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
              required
            />
          </div>

          {/* Smoker */}
          <div>
            <label htmlFor="smoker" className="block text-sm font-medium text-gray-700 mb-2">
              Smoker
            </label>
            <select
              id="smoker"
              name="smoker"
              value={formData.smoker}
              onChange={handleInputChange}
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
            >
              <option value="no">No</option>
              <option value="yes">Yes</option>
            </select>
          </div>

          {/* Region */}
          <div>
            <label htmlFor="region" className="block text-sm font-medium text-gray-700 mb-2">
              Region
            </label>
            <select
              id="region"
              name="region"
              value={formData.region}
              onChange={handleInputChange}
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
            >
              <option value="southeast">Southeast</option>
              <option value="southwest">Southwest</option>
              <option value="northeast">Northeast</option>
              <option value="northwest">Northwest</option>
            </select>
          </div>
        </div>

        <button
          type="submit"
          disabled={loading}
          className="w-full bg-primary-600 text-white py-3 px-4 rounded-lg font-medium hover:bg-primary-700 focus:ring-2 focus:ring-primary-500 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center"
        >
          {loading ? (
            <>
              <Loader className="w-5 h-5 mr-2 animate-spin" />
              Calculating...
            </>
          ) : (
            <>
              <Calculator className="w-5 h-5 mr-2" />
              Calculate Insurance Premium
            </>
          )}
        </button>
      </form>

      {/* Results */}
      {error && (
        <div className="bg-red-50 border border-red-200 rounded-lg p-4">
          <div className="flex items-center">
            <AlertCircle className="w-5 h-5 text-red-600 mr-2" />
            <p className="text-red-800">{error}</p>
          </div>
        </div>
      )}

      {prediction && (
        <div className="space-y-4">
          <div className="bg-green-50 border border-green-200 rounded-lg p-6">
            <div className="flex items-center mb-4">
              <CheckCircle className="w-6 h-6 text-green-600 mr-2" />
              <h3 className="text-lg font-semibold text-green-800">
                Estimated Insurance Premium
              </h3>
            </div>
            <div className="text-3xl font-bold text-green-700 mb-2">
              ₹{prediction.estimated_price.toLocaleString('en-IN', { maximumFractionDigits: 2 })}
            </div>
            <p className="text-green-600">
              Based on your profile, this is the estimated annual premium for health insurance.
            </p>
          </div>

          {/* Get Recommendations Button */}
          <div className="flex justify-center">
            <button
              onClick={handleGetRecommendations}
              disabled={recommendationsLoading}
              className="bg-blue-600 text-white py-3 px-6 rounded-lg font-medium hover:bg-blue-700 focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed flex items-center"
            >
              {recommendationsLoading ? (
                <>
                  <Loader className="w-5 h-5 mr-2 animate-spin" />
                  Getting Recommendations...
                </>
              ) : (
                <>
                  <Calculator className="w-5 h-5 mr-2" />
                  Get Recommended Plans
                </>
              )}
            </button>
          </div>

          {/* Recommendations Display */}
          {recommendations && (
            <div className="bg-blue-50 border border-blue-200 rounded-lg p-6 relative">
              <button
                onClick={handleCloseRecommendations}
                className="absolute top-4 right-4 text-blue-600 hover:text-blue-800 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 rounded-full p-1"
                aria-label="Close recommendations"
              >
                <X className="w-5 h-5" />
              </button>
              <h3 className="text-lg font-semibold text-blue-800 mb-4 pr-8">
                Recommended Insurance Plans
              </h3>
              <div className="prose prose-blue max-w-none">
                <div 
                  className="text-blue-700 whitespace-pre-line"
                  dangerouslySetInnerHTML={{ 
                    __html: recommendations.replace(/\n/g, '<br/>') 
                  }}
                />
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );
};

export default InsuranceForm;
