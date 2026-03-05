import React, { useEffect, useState } from 'react';
import { Database, Table, Key, Link } from 'lucide-react';

interface TableInfo {
  name: string;
  columns: ColumnInfo[];
}

interface ColumnInfo {
  name: string;
  type: string;
  nullable: boolean;
  primary_key: boolean;
  foreign_key?: string;
}

interface SchemaViewerProps {
  onClose?: () => void;
}

const SchemaViewer: React.FC<SchemaViewerProps> = ({ onClose }) => {
  const [schema, setSchema] = useState<TableInfo[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [selectedTable, setSelectedTable] = useState<string | null>(null);

  useEffect(() => {
    fetchSchema();
  }, []);

  const fetchSchema = async () => {
    try {
      setLoading(true);
      const response = await fetch('http://localhost:8000/api/schema');
      const data = await response.json();
      
      if (data.success) {
        // Parse the schema text into structured data
        const tables = parseSchemaText(data.schema);
        setSchema(tables);
        if (tables.length > 0) {
          setSelectedTable(tables[0].name);
        }
      } else {
        setError('Failed to load schema');
      }
    } catch (err) {
      setError('Error fetching schema: ' + (err as Error).message);
    } finally {
      setLoading(false);
    }
  };

  const parseSchemaText = (schemaText: string): TableInfo[] => {
    const tables: TableInfo[] = [];
    const tableBlocks = schemaText.split(/CREATE TABLE/i).slice(1);

    tableBlocks.forEach(block => {
      const tableNameMatch = block.match(/["']?(\w+)["']?\s*\(/);
      if (!tableNameMatch) return;

      const tableName = tableNameMatch[1];
      const columns: ColumnInfo[] = [];

      // Extract column definitions
      const columnSection = block.match(/\(([\s\S]*?)\)/)?.[1] || '';
      const columnLines = columnSection.split(',').map(line => line.trim());

      columnLines.forEach(line => {
        if (!line || line.toUpperCase().startsWith('PRIMARY KEY') || 
            line.toUpperCase().startsWith('FOREIGN KEY') ||
            line.toUpperCase().startsWith('UNIQUE') ||
            line.toUpperCase().startsWith('CHECK')) {
          return;
        }

        const parts = line.split(/\s+/);
        if (parts.length < 2) return;

        const columnName = parts[0].replace(/["']/g, '');
        const columnType = parts[1].toUpperCase();
        const isPrimaryKey = line.toUpperCase().includes('PRIMARY KEY');
        const isNullable = !line.toUpperCase().includes('NOT NULL');
        
        // Check for foreign key
        const fkMatch = line.match(/REFERENCES\s+(\w+)/i);
        const foreignKey = fkMatch ? fkMatch[1] : undefined;

        columns.push({
          name: columnName,
          type: columnType,
          nullable: isNullable,
          primary_key: isPrimaryKey,
          foreign_key: foreignKey
        });
      });

      if (columns.length > 0) {
        tables.push({ name: tableName, columns });
      }
    });

    return tables;
  };

  const selectedTableData = schema.find(t => t.name === selectedTable);

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="bg-red-50 border border-red-200 rounded-lg p-4">
        <p className="text-red-800">{error}</p>
      </div>
    );
  }

  return (
    <div className="bg-white rounded-lg shadow-lg">
      <div className="border-b border-gray-200 p-4 flex items-center justify-between">
        <div className="flex items-center gap-2">
          <Database className="w-6 h-6 text-blue-600" />
          <h2 className="text-xl font-bold text-gray-900">Database Schema</h2>
        </div>
        {onClose && (
          <button
            onClick={onClose}
            className="text-gray-500 hover:text-gray-700"
          >
            ✕
          </button>
        )}
      </div>

      <div className="flex h-[600px]">
        {/* Table List */}
        <div className="w-64 border-r border-gray-200 overflow-y-auto">
          <div className="p-4">
            <h3 className="text-sm font-semibold text-gray-700 mb-3">Tables ({schema.length})</h3>
            <div className="space-y-1">
              {schema.map(table => (
                <button
                  key={table.name}
                  onClick={() => setSelectedTable(table.name)}
                  className={`w-full text-left px-3 py-2 rounded-lg flex items-center gap-2 transition-colors ${
                    selectedTable === table.name
                      ? 'bg-blue-50 text-blue-700 font-medium'
                      : 'text-gray-700 hover:bg-gray-50'
                  }`}
                >
                  <Table className="w-4 h-4" />
                  <span className="truncate">{table.name}</span>
                </button>
              ))}
            </div>
          </div>
        </div>

        {/* Table Details */}
        <div className="flex-1 overflow-y-auto p-6">
          {selectedTableData ? (
            <div>
              <div className="mb-6">
                <h3 className="text-2xl font-bold text-gray-900 mb-2">
                  {selectedTableData.name}
                </h3>
                <p className="text-gray-600">
                  {selectedTableData.columns.length} columns
                </p>
              </div>

              <div className="bg-gray-50 rounded-lg overflow-hidden">
                <table className="w-full">
                  <thead className="bg-gray-100 border-b border-gray-200">
                    <tr>
                      <th className="px-4 py-3 text-left text-xs font-semibold text-gray-700 uppercase">
                        Column
                      </th>
                      <th className="px-4 py-3 text-left text-xs font-semibold text-gray-700 uppercase">
                        Type
                      </th>
                      <th className="px-4 py-3 text-left text-xs font-semibold text-gray-700 uppercase">
                        Constraints
                      </th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-gray-200">
                    {selectedTableData.columns.map((column, idx) => (
                      <tr key={idx} className="hover:bg-white transition-colors">
                        <td className="px-4 py-3">
                          <div className="flex items-center gap-2">
                            {column.primary_key && (
                              <div title="Primary Key">
                                <Key className="w-4 h-4 text-yellow-600" />
                              </div>
                            )}
                            {column.foreign_key && (
                              <div title={`References ${column.foreign_key}`}>
                                <Link className="w-4 h-4 text-blue-600" />
                              </div>
                            )}
                            <span className="font-mono text-sm font-medium text-gray-900">
                              {column.name}
                            </span>
                          </div>
                        </td>
                        <td className="px-4 py-3">
                          <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-blue-100 text-blue-800">
                            {column.type}
                          </span>
                        </td>
                        <td className="px-4 py-3">
                          <div className="flex flex-wrap gap-1">
                            {column.primary_key && (
                              <span className="inline-flex items-center px-2 py-0.5 rounded text-xs font-medium bg-yellow-100 text-yellow-800">
                                PRIMARY KEY
                              </span>
                            )}
                            {!column.nullable && (
                              <span className="inline-flex items-center px-2 py-0.5 rounded text-xs font-medium bg-red-100 text-red-800">
                                NOT NULL
                              </span>
                            )}
                            {column.foreign_key && (
                              <span className="inline-flex items-center px-2 py-0.5 rounded text-xs font-medium bg-blue-100 text-blue-800">
                                FK → {column.foreign_key}
                              </span>
                            )}
                          </div>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>

              {/* Relationships */}
              {selectedTableData.columns.some(c => c.foreign_key) && (
                <div className="mt-6">
                  <h4 className="text-lg font-semibold text-gray-900 mb-3">Relationships</h4>
                  <div className="space-y-2">
                    {selectedTableData.columns
                      .filter(c => c.foreign_key)
                      .map((column, idx) => (
                        <div
                          key={idx}
                          className="flex items-center gap-2 p-3 bg-blue-50 rounded-lg"
                        >
                          <Link className="w-4 h-4 text-blue-600" />
                          <span className="text-sm text-gray-700">
                            <span className="font-mono font-medium">{column.name}</span>
                            {' → '}
                            <span className="font-mono font-medium text-blue-600">
                              {column.foreign_key}
                            </span>
                          </span>
                        </div>
                      ))}
                  </div>
                </div>
              )}
            </div>
          ) : (
            <div className="flex items-center justify-center h-full text-gray-500">
              Select a table to view its schema
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default SchemaViewer;

// Made with Bob
