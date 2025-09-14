import React, { useState } from 'react';
import InsuranceForm from './components/InsuranceForm';
import Chatbot from './components/Chatbot';
import { MessageCircle, Calculator } from 'lucide-react';

function App() {
  const [activeTab, setActiveTab] = useState('insurance');

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      {/* Header */}
      <header className="bg-white shadow-lg">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center py-6">
            <div className="flex items-center">
              <div className="flex-shrink-0">
                <h1 className="text-3xl font-bold text-gray-900">
                  Health Insurance System
                </h1>
              </div>
            </div>
            <div className="flex space-x-4">
              <button
                onClick={() => setActiveTab('insurance')}
                className={`flex items-center px-4 py-2 rounded-lg font-medium transition-colors ${
                  activeTab === 'insurance'
                    ? 'bg-primary-600 text-white'
                    : 'text-gray-600 hover:text-primary-600 hover:bg-primary-50'
                }`}
              >
                <Calculator className="w-5 h-5 mr-2" />
                Insurance Calculator
              </button>
              <button
                onClick={() => setActiveTab('chatbot')}
                className={`flex items-center px-4 py-2 rounded-lg font-medium transition-colors ${
                  activeTab === 'chatbot'
                    ? 'bg-primary-600 text-white'
                    : 'text-gray-600 hover:text-primary-600 hover:bg-primary-50'
                }`}
              >
                <MessageCircle className="w-5 h-5 mr-2" />
                AI Chatbot
              </button>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Main Content Area */}
          <div className="lg:col-span-2">
            <div className="bg-white rounded-xl shadow-lg p-8">
              {activeTab === 'insurance' ? (
                <div>
                  <div className="flex items-center mb-6">
                    <Calculator className="w-6 h-6 text-primary-600 mr-2" />
                    <h2 className="text-2xl font-semibold text-gray-900">
                      Insurance Premium Calculator
                    </h2>
                  </div>
                  <InsuranceForm />
                </div>
              ) : (
                <div>
                  <div className="flex items-center mb-6">
                    <MessageCircle className="w-6 h-6 text-primary-600 mr-2" />
                    <h2 className="text-2xl font-semibold text-gray-900">
                      Chat with Insurance Expert
                    </h2>
                  </div>
                  <div className="text-center py-12">
                    <MessageCircle className="w-16 h-16 text-gray-400 mx-auto mb-4" />
                    <p className="text-gray-600">
                      Use the chatbot on the right to ask questions about insurance.
                    </p>
                  </div>
                </div>
              )}
            </div>
          </div>

          {/* Chatbot Sidebar - Right Side */}
          <div className="lg:col-span-1 min-h-0">
            <div className="bg-white rounded-xl shadow-lg p-6 h-[80vh] overflow-hidden flex flex-col">
              <div className="flex items-center mb-4">
                <MessageCircle className="w-6 h-6 text-primary-600 mr-2" />
                <h2 className="text-xl font-semibold text-gray-900">
                  Insurance Assistant
                </h2>
              </div>
              <p className="text-gray-600 mb-4">
                Ask me about health insurance terms, policies, and laws in India.
              </p>
              <div className="flex-1 min-h-0">
                <Chatbot />
              </div>
            </div>
          </div>
        </div>
      </main>

      {/* Footer */}
      <footer className="bg-white border-t mt-12">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <div className="text-center text-gray-600">
            <p>&copy; 2024 Health Insurance System. All rights reserved.</p>
          </div>
        </div>
      </footer>
    </div>
  );
}

export default App;
