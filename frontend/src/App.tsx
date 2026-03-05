import React, { useState, useEffect } from 'react';
import { Brain, AlertCircle, Database } from 'lucide-react';
import ChatInterface from './components/ChatInterface';
import ResultDisplay from './components/ResultDisplay';
import SchemaViewer from './components/SchemaViewer';
import { sendQuery, getSampleQueries } from './services/api';
import type { QueryResponse } from './types';

function App() {
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [currentResponse, setCurrentResponse] = useState<QueryResponse | null>(null);
  const [sampleQueries, setSampleQueries] = useState<string[]>([]);
  const [showSchema, setShowSchema] = useState(false);

  // Load sample queries on mount
  useEffect(() => {
    const loadSamples = async () => {
      try {
        const queries = await getSampleQueries();
        setSampleQueries(queries);
      } catch (err) {
        console.error('Failed to load sample queries:', err);
      }
    };
    loadSamples();
  }, []);

  const handleQuery = async (question: string) => {
    setIsLoading(true);
    setError(null);

    try {
      const response = await sendQuery(question);
      setCurrentResponse(response);
    } catch (err: any) {
      const errorMessage = err.response?.data?.detail || err.message || 'Failed to process query';
      setError(errorMessage);
      setCurrentResponse(null);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-purple-50">
      {/* Header */}
      <header className="bg-white border-b border-gray-200 shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <div className="p-2 bg-primary-500 rounded-lg">
                <Brain className="w-6 h-6 text-white" />
              </div>
              <div>
                <h1 className="text-2xl font-bold text-gray-900">AI Analytics</h1>
                <p className="text-sm text-gray-600">Ask questions about your data in natural language</p>
              </div>
            </div>
            <button
              onClick={() => setShowSchema(!showSchema)}
              className="flex items-center gap-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
            >
              <Database className="w-5 h-5" />
              <span>{showSchema ? 'Hide' : 'View'} Schema</span>
            </button>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="space-y-8">
          {/* Schema Viewer Modal */}
          {showSchema && (
            <div className="fixed inset-0 bg-black bg-opacity-50 z-50 flex items-center justify-center p-4">
              <div className="max-w-6xl w-full max-h-[90vh] overflow-hidden">
                <SchemaViewer onClose={() => setShowSchema(false)} />
              </div>
            </div>
          )}

          {/* Chat Interface */}
          <ChatInterface
            onSubmit={handleQuery}
            isLoading={isLoading}
            sampleQueries={sampleQueries}
          />

          {/* Error Display */}
          {error && (
            <div className="bg-red-50 border border-red-200 rounded-lg p-4">
              <div className="flex items-start gap-3">
                <AlertCircle className="w-5 h-5 text-red-500 flex-shrink-0 mt-0.5" />
                <div>
                  <h3 className="font-semibold text-red-900 mb-1">Error</h3>
                  <p className="text-red-700">{error}</p>
                </div>
              </div>
            </div>
          )}

          {/* Loading State */}
          {isLoading && (
            <div className="bg-blue-50 border border-blue-200 rounded-lg p-8">
              <div className="flex flex-col items-center justify-center gap-4">
                <div className="relative">
                  <div className="w-16 h-16 border-4 border-blue-200 rounded-full"></div>
                  <div className="absolute top-0 left-0 w-16 h-16 border-4 border-blue-500 rounded-full border-t-transparent animate-spin"></div>
                </div>
                <div className="text-center">
                  <p className="text-lg font-medium text-blue-900">Processing your query...</p>
                  <p className="text-sm text-blue-700 mt-1">AI is analyzing your data</p>
                </div>
              </div>
            </div>
          )}

          {/* Results Display */}
          {currentResponse && !isLoading && (
            <div className="animate-fadeIn">
              <ResultDisplay response={currentResponse} />
            </div>
          )}

          {/* Welcome Message */}
          {!currentResponse && !isLoading && !error && (
            <div className="text-center py-12">
              <div className="inline-flex items-center justify-center w-20 h-20 bg-primary-100 rounded-full mb-4">
                <Brain className="w-10 h-10 text-primary-600" />
              </div>
              <h2 className="text-2xl font-bold text-gray-900 mb-2">
                Welcome to AI Analytics
              </h2>
              <p className="text-gray-600 max-w-2xl mx-auto">
                Ask questions about your e-commerce data in plain English. 
                The AI will generate SQL queries, analyze results, and create visualizations automatically.
              </p>
              <div className="mt-8 grid grid-cols-1 md:grid-cols-3 gap-4 max-w-4xl mx-auto">
                <div className="bg-white rounded-lg p-6 shadow-sm border border-gray-200">
                  <div className="text-3xl mb-2">📊</div>
                  <h3 className="font-semibold text-gray-900 mb-1">Smart Analysis</h3>
                  <p className="text-sm text-gray-600">AI-powered insights and trend identification</p>
                </div>
                <div className="bg-white rounded-lg p-6 shadow-sm border border-gray-200">
                  <div className="text-3xl mb-2">📈</div>
                  <h3 className="font-semibold text-gray-900 mb-1">Auto Visualization</h3>
                  <p className="text-sm text-gray-600">Dynamic charts based on your data</p>
                </div>
                <div className="bg-white rounded-lg p-6 shadow-sm border border-gray-200">
                  <div className="text-3xl mb-2">🔒</div>
                  <h3 className="font-semibold text-gray-900 mb-1">Safe & Secure</h3>
                  <p className="text-sm text-gray-600">Read-only queries with validation</p>
                </div>
              </div>
            </div>
          )}
        </div>
      </main>

      {/* Footer */}
      <footer className="mt-16 border-t border-gray-200 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <p className="text-center text-sm text-gray-600">
            Powered by OpenAI GPT-4, LangChain, and FastAPI
          </p>
        </div>
      </footer>
    </div>
  );
}

export default App;

// Made with Bob
