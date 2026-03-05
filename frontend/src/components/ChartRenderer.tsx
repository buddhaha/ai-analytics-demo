import React from 'react';
import {
  BarChart,
  Bar,
  LineChart,
  Line,
  PieChart,
  Pie,
  Cell,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from 'recharts';
import type { VisualizationConfig } from '../types';

interface ChartRendererProps {
  config: VisualizationConfig;
}

const COLORS = [
  '#0ea5e9', '#8b5cf6', '#ec4899', '#f59e0b', '#10b981',
  '#6366f1', '#ef4444', '#14b8a6', '#f97316', '#84cc16'
];

const ChartRenderer: React.FC<ChartRendererProps> = ({ config }) => {
  if (config.type === 'none' || !config.data || config.data.length === 0) {
    return (
      <div className="flex items-center justify-center h-64 bg-gray-50 rounded-lg border-2 border-dashed border-gray-300">
        <p className="text-gray-500">No visualization available</p>
      </div>
    );
  }

  if (config.type === 'table') {
    return <TableView data={config.data} columns={config.columns || []} />;
  }

  return (
    <div className="w-full h-96 bg-white rounded-lg p-4 shadow-sm border border-gray-200">
      <ResponsiveContainer width="100%" height="100%">
        <>
          {config.type === 'bar' && (
            <BarChart data={config.data}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey={config.xAxis} />
              <YAxis />
              <Tooltip />
              <Legend />
              <Bar dataKey={config.yAxis || 'value'} fill="#0ea5e9" />
            </BarChart>
          )}

          {config.type === 'line' && (
            <LineChart data={config.data}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey={config.xAxis} />
              <YAxis />
              <Tooltip />
              <Legend />
              <Line
                type="monotone"
                dataKey={config.yAxis}
                stroke="#0ea5e9"
                strokeWidth={2}
                dot={{ fill: '#0ea5e9' }}
              />
            </LineChart>
          )}

          {config.type === 'pie' && (
            <PieChart>
              <Pie
                data={config.data}
                dataKey={config.valueKey || 'value'}
                nameKey={config.nameKey}
                cx="50%"
                cy="50%"
                outerRadius={120}
                label
              >
                {config.data.map((_, index) => (
                  <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                ))}
              </Pie>
              <Tooltip />
              <Legend />
            </PieChart>
          )}
        </>
      </ResponsiveContainer>
    </div>
  );
};

interface TableViewProps {
  data: Record<string, any>[];
  columns: string[];
}

const TableView: React.FC<TableViewProps> = ({ data, columns }) => {
  const displayColumns = columns.length > 0 ? columns : Object.keys(data[0] || {});

  return (
    <div className="overflow-x-auto rounded-lg border border-gray-200 shadow-sm">
      <table className="min-w-full divide-y divide-gray-200">
        <thead className="bg-gray-50">
          <tr>
            {displayColumns.map((column) => (
              <th
                key={column}
                className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
              >
                {column}
              </th>
            ))}
          </tr>
        </thead>
        <tbody className="bg-white divide-y divide-gray-200">
          {data.map((row, rowIndex) => (
            <tr key={rowIndex} className="hover:bg-gray-50">
              {displayColumns.map((column) => (
                <td key={column} className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                  {formatValue(row[column])}
                </td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

const formatValue = (value: any): string => {
  if (value === null || value === undefined) return '-';
  if (typeof value === 'number') {
    return value.toLocaleString();
  }
  return String(value);
};

export default ChartRenderer;

// Made with Bob
