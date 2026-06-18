import React from 'react';
import {
  BarChart,
  Bar,
  LineChart,
  Line,
  PieChart,
  Pie,
  Cell,
  AreaChart,
  Area,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from 'recharts';
import { Lightbulb, Table } from 'lucide-react';

interface VisualizationConfig {
  type: 'bar' | 'line' | 'pie' | 'area';
  xKey: string;
  yKey: string;
}

interface ResultsDisplayProps {
  results: any[];
  visualization: VisualizationConfig | null;
  interpretation: string;
}

const COLORS = [
  '#06b6d4', // cyan
  '#3b82f6', // blue
  '#8b5cf6', // violet
  '#ec4899', // pink
  '#f59e0b', // amber
  '#10b981', // emerald
  '#6366f1', // indigo
  '#ef4444', // red
];

export const ResultsDisplay: React.FC<ResultsDisplayProps> = ({
  results,
  visualization,
  interpretation,
}) => {
  const [showTable, setShowTable] = React.useState(false);

  const renderChart = () => {
    if (!visualization) return null;

    const { type, xKey, yKey } = visualization;

    try {
      switch (type) {
        case 'bar':
          return (
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={results}>
                <CartesianGrid strokeDasharray="3 3" stroke="#475569" />
                <XAxis dataKey={xKey} stroke="#94a3b8" />
                <YAxis stroke="#94a3b8" />
                <Tooltip
                  contentStyle={{
                    backgroundColor: '#1e293b',
                    border: '1px solid #475569',
                    borderRadius: '8px',
                  }}
                  labelStyle={{ color: '#e2e8f0' }}
                />
                <Legend />
                <Bar dataKey={yKey} fill="#06b6d4" radius={[8, 8, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          );

        case 'line':
          return (
            <ResponsiveContainer width="100%" height={300}>
              <LineChart data={results}>
                <CartesianGrid strokeDasharray="3 3" stroke="#475569" />
                <XAxis dataKey={xKey} stroke="#94a3b8" />
                <YAxis stroke="#94a3b8" />
                <Tooltip
                  contentStyle={{
                    backgroundColor: '#1e293b',
                    border: '1px solid #475569',
                    borderRadius: '8px',
                  }}
                  labelStyle={{ color: '#e2e8f0' }}
                />
                <Legend />
                <Line
                  type="monotone"
                  dataKey={yKey}
                  stroke="#06b6d4"
                  dot={{ fill: '#06b6d4' }}
                  strokeWidth={2}
                />
              </LineChart>
            </ResponsiveContainer>
          );

        case 'pie':
          return (
            <ResponsiveContainer width="100%" height={300}>
              <PieChart>
                <Pie
                  data={results}
                  dataKey={yKey}
                  nameKey={xKey}
                  cx="50%"
                  cy="50%"
                  outerRadius={100}
                  label
                >
                  {results.map((_, index) => (
                    <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                  ))}
                </Pie>
                <Tooltip
                  contentStyle={{
                    backgroundColor: '#1e293b',
                    border: '1px solid #475569',
                    borderRadius: '8px',
                  }}
                  labelStyle={{ color: '#e2e8f0' }}
                />
              </PieChart>
            </ResponsiveContainer>
          );

        case 'area':
          return (
            <ResponsiveContainer width="100%" height={300}>
              <AreaChart data={results}>
                <CartesianGrid strokeDasharray="3 3" stroke="#475569" />
                <XAxis dataKey={xKey} stroke="#94a3b8" />
                <YAxis stroke="#94a3b8" />
                <Tooltip
                  contentStyle={{
                    backgroundColor: '#1e293b',
                    border: '1px solid #475569',
                    borderRadius: '8px',
                  }}
                  labelStyle={{ color: '#e2e8f0' }}
                />
                <Legend />
                <Area
                  type="monotone"
                  dataKey={yKey}
                  stroke="#06b6d4"
                  fill="#06b6d4"
                  fillOpacity={0.3}
                />
              </AreaChart>
            </ResponsiveContainer>
          );

        default:
          return null;
      }
    } catch (error) {
      return (
        <div className="bg-red-500/10 border border-red-500/30 rounded p-4 text-red-300 text-sm">
          Could not render visualization
        </div>
      );
    }
  };

  return (
    <div className="space-y-6">
      {/* Visualization */}
      {visualization && (
        <div className="bg-slate-800 border border-slate-700 rounded-lg p-6">
          <h3 className="text-white font-semibold mb-4">Data Visualization</h3>
          <div className="bg-slate-900/50 rounded p-4 overflow-x-auto">
            {renderChart()}
          </div>
        </div>
      )}

      {/* Interpretation */}
      <div className="bg-gradient-to-r from-blue-500/10 to-cyan-500/10 border border-blue-500/30 rounded-lg p-4 flex gap-3">
        <Lightbulb className="h-5 w-5 text-blue-400 flex-shrink-0 mt-0.5" />
        <div>
          <h3 className="text-white font-semibold mb-2">Analysis & Interpretation</h3>
          <div className="text-slate-200 text-sm leading-relaxed whitespace-pre-wrap">
            {interpretation}
          </div>
        </div>
      </div>

      {/* Data Table */}
      <div className="bg-slate-800 border border-slate-700 rounded-lg">
        <button
          onClick={() => setShowTable(!showTable)}
          className="w-full px-4 py-3 flex items-center gap-2 hover:bg-slate-700/50 transition-colors"
        >
          <Table className="h-4 w-4 text-slate-400" />
          <span className="text-white font-medium">
            View Data Table ({results.length} rows)
          </span>
        </button>

        {showTable && (
          <div className="border-t border-slate-700 overflow-x-auto">
            <table className="w-full text-sm">
              <thead className="bg-slate-900/50 sticky top-0">
                <tr>
                  {Object.keys(results[0] || {}).map((key) => (
                    <th
                      key={key}
                      className="px-4 py-3 text-left text-slate-300 font-semibold"
                    >
                      {key}
                    </th>
                  ))}
                </tr>
              </thead>
              <tbody>
                {results.map((row, idx) => (
                  <tr
                    key={idx}
                    className="border-t border-slate-700 hover:bg-slate-700/30 transition-colors"
                  >
                    {Object.values(row).map((value: any, cellIdx) => (
                      <td
                        key={`${idx}-${cellIdx}`}
                        className="px-4 py-3 text-slate-200"
                      >
                        {typeof value === 'number'
                          ? value.toLocaleString()
                          : String(value)}
                      </td>
                    ))}
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>

      {/* Metadata */}
      <div className="bg-slate-800 border border-slate-700 rounded-lg p-4">
        <h4 className="text-slate-300 font-semibold text-sm mb-2">Query Information</h4>
        <div className="grid grid-cols-3 gap-4">
          <div>
            <p className="text-slate-500 text-xs mb-1">Rows Returned</p>
            <p className="text-white font-semibold">{results.length}</p>
          </div>
          <div>
            <p className="text-slate-500 text-xs mb-1">Columns</p>
            <p className="text-white font-semibold">
              {Object.keys(results[0] || {}).length}
            </p>
          </div>
          <div>
            <p className="text-slate-500 text-xs mb-1">Status</p>
            <p className="text-emerald-400 font-semibold">Successful</p>
          </div>
        </div>
      </div>
    </div>
  );
};
