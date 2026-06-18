import React from 'react';
import { Sparkles } from 'lucide-react';

interface SampleQuestionsProps {
  onSelectQuestion: (question: string) => void;
}

export const SampleQuestions: React.FC<SampleQuestionsProps> = ({ onSelectQuestion }) => {
  const sampleQuestions = [
    'What were the total sales by product category?',
    'Show me the top 5 products by revenue',
    'What is the daily revenue trend?',
    'How much revenue did each customer segment generate?',
    'What is the average price by product category?',
    'Which products had the highest sales volume?',
  ];

  return (
    <div className="space-y-3">
      <div className="flex items-center gap-2">
        <Sparkles className="h-4 w-4 text-blue-400" />
        <p className="text-sm text-slate-400">Try asking about your data:</p>
      </div>
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-2">
        {sampleQuestions.map((question, idx) => (
          <button
            key={idx}
            onClick={() => onSelectQuestion(question)}
            className="text-left px-3 py-2 bg-slate-700 hover:bg-slate-600 text-slate-200 hover:text-white rounded-lg transition-all text-sm border border-slate-600 hover:border-slate-500"
          >
            {question}
          </button>
        ))}
      </div>
    </div>
  );
};
