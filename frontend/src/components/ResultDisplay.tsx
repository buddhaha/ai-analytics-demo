import React from 'react';
import { CheckCircle2, XCircle, Database, Code, Lightbulb, Table } from 'lucide-react';
import ChartRenderer from './ChartRenderer';
import type { QueryResponse } from '../types';

interface ResultDisplayProps {
  response: QueryResponse;
}

const ResultDisplay: React.FC<ResultDisplayProps> = ({ response }) => {
  // Debug logging
  console.log('ResultDisplay received response:', response);
  console.log('SQL:', response.sql);
  console.log('Results:', response.results);
  console.log('Results length:', response.results?.length);
  
  if (!response.success) {
    return (
      <div className="bg-red-50 border border-red-200 rounded-lg p-6">
        <div className="flex items-start gap-3">
          <XCircle className="w-6 h-6 text-red-500 flex-shrink-0 mt-0.5" />
          <div>
            <h3 className="font-semibold text-red-900 mb-2">Error Processing Query</h3>
            <p className="text-red-700">{response.error || 'An unknown error occurred'}</p>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Success Header */}
      <div className="flex items-center gap-2 text-green-600">
        <CheckCircle2 className="w-5 h-5" />
        <span className="font-medium">Query executed successfully</span>
        <span className="text-sm text-gray-500">({response.row_count} rows)</span>
      </div>

      {/* Question */}
      <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
        <div className="flex items-start gap-3">
          <Database className="w-5 h-5 text-blue-600 flex-shrink-0 mt-0.5" />
          <div>
            <p className="text-sm font-medium text-blue-900 mb-1">Question</p>
            <p className="text-blue-800">{response.question}</p>
          </div>
        </div>
      </div>

      {/* SQL Query */}
      {response.sql && (
        <div className="bg-gray-50 border border-gray-200 rounded-lg p-4">
          <div className="flex items-start gap-3">
            <Code className="w-5 h-5 text-gray-600 flex-shrink-0 mt-0.5" />
            <div className="flex-1 min-w-0">
              <p className="text-sm font-medium text-gray-900 mb-2">Generated SQL</p>
              <pre className="text-sm text-gray-800 bg-white p-3 rounded border border-gray-200 overflow-x-auto">
                <code>{response.sql}</code>
              </pre>
            </div>
          </div>
        </div>
      )}

      {/* Raw Results Table */}
      {response.results && response.results.length > 0 && (
        <div className="bg-white border border-gray-200 rounded-lg p-4">
          <div className="flex items-start gap-3 mb-4">
            <Table className="w-5 h-5 text-gray-600 flex-shrink-0 mt-0.5" />
            <div>
              <p className="text-sm font-medium text-gray-900">Raw Results</p>
              <p className="text-xs text-gray-500">{response.row_count} rows returned</p>
            </div>
          </div>
          <div className="overflow-x-auto">
            <table className="min-w-full divide-y divide-gray-200">
              <thead className="bg-gray-50">
                <tr>
                  {Object.keys(response.results[0]).map((column) => (
                    <th
                      key={column}
                      className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
                    >
                      {column}
                    </th>
                  ))}
                </tr>
              </thead>
              <tbody className="bg-white divide-y divide-gray-200">
                {response.results.slice(0, 100).map((row, rowIndex) => (
                  <tr key={rowIndex} className="hover:bg-gray-50">
                    {Object.values(row).map((value, colIndex) => (
                      <td
                        key={colIndex}
                        className="px-4 py-3 text-sm text-gray-900 whitespace-nowrap"
                      >
                        {value === null ? (
                          <span className="text-gray-400 italic">null</span>
                        ) : typeof value === 'object' ? (
                          JSON.stringify(value)
                        ) : (
                          String(value)
                        )}
                      </td>
                    ))}
                  </tr>
                ))}
              </tbody>
            </table>
            {response.results.length > 100 && (
              <div className="mt-3 text-sm text-gray-500 text-center">
                Showing first 100 of {response.results.length} rows
              </div>
            )}
          </div>
        </div>
      )}

      {/* Visualization */}
      {response.visualization && response.visualization.type !== 'none' && (
        <div>
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Visualization</h3>
          <ChartRenderer config={response.visualization} />
        </div>
      )}

      {/* AI Analysis */}
      {response.analysis && (
        <div className="bg-purple-50 border border-purple-200 rounded-lg p-4">
          <div className="flex items-start gap-3">
            <Lightbulb className="w-5 h-5 text-purple-600 flex-shrink-0 mt-0.5" />
            <div>
              <p className="text-sm font-medium text-purple-900 mb-2">AI Insights</p>
              <div className="text-purple-800 whitespace-pre-wrap">{response.analysis}</div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default ResultDisplay;

// Made with Bob
