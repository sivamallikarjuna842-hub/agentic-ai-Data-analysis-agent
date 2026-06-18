import React from 'react';
import { ChevronDown, Copy, Check } from 'lucide-react';
import { useState } from 'react';

interface QueryPreviewProps {
  question: string;
  sql: string;
  onToggle: (isExpanded: boolean) => void;
  isExpanded: boolean;
}

export const QueryPreview: React.FC<QueryPreviewProps> = ({
  question,
  sql,
  onToggle,
  isExpanded,
}) => {
  const [copied, setCopied] = useState(false);

  const handleCopy = () => {
    navigator.clipboard.writeText(sql);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <div className="bg-slate-800 border border-slate-700 rounded-lg overflow-hidden">
      <button
        onClick={() => onToggle(!isExpanded)}
        className="w-full px-4 py-3 flex items-center justify-between hover:bg-slate-700/50 transition-colors"
      >
        <div className="flex items-center gap-3 flex-1 text-left">
          <ChevronDown
            className={`h-5 w-5 text-slate-400 transition-transform ${
              isExpanded ? 'rotate-180' : ''
            }`}
          />
          <div>
            <p className="text-sm text-slate-400">Question Asked</p>
            <p className="text-white font-medium">{question}</p>
          </div>
        </div>
      </button>

      {isExpanded && (
        <div className="border-t border-slate-700 px-4 py-4 bg-slate-900/50">
          <div className="space-y-3">
            <div>
              <p className="text-sm text-slate-400 mb-2">Generated SQL Query</p>
              <div className="relative">
                <pre className="bg-slate-950 border border-slate-700 rounded p-3 text-cyan-300 text-sm overflow-x-auto max-h-40 font-mono">
                  {sql}
                </pre>
                <button
                  onClick={handleCopy}
                  className="absolute top-2 right-2 p-2 bg-slate-700 hover:bg-slate-600 text-slate-300 rounded transition-colors"
                  title="Copy SQL"
                >
                  {copied ? (
                    <Check className="h-4 w-4 text-green-400" />
                  ) : (
                    <Copy className="h-4 w-4" />
                  )}
                </button>
              </div>
            </div>
            <p className="text-xs text-slate-500">
              This SQL was automatically generated from your natural language question. Review it to ensure it matches your intent.
            </p>
          </div>
        </div>
      )}
    </div>
  );
};
