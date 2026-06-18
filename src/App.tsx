import React, { useState, useRef } from 'react';
import { Send, Loader, Database, TrendingUp, AlertCircle } from 'lucide-react';
import { DataAnalystAgent, AnalysisResult } from './components/DataAnalystAgent';
import { QueryPreview } from './components/QueryPreview';
import { ResultsDisplay } from './components/ResultsDisplay';
import { SampleQuestions } from './components/SampleQuestions';

export default function App() {
  const [question, setQuestion] = useState('');
  const [analysis, setAnalysis] = useState<AnalysisResult | null>(null);
  const [loading, setLoading] = useState(false);
  const [showPreview, setShowPreview] = useState(false);
  const [conversationHistory, setConversationHistory] = useState<AnalysisResult[]>([]);
  const scrollRef = useRef<HTMLDivElement>(null);
  const agentRef = useRef<DataAnalystAgent>(new DataAnalystAgent());

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!question.trim()) return;

    setLoading(true);
    setShowPreview(false);

    try {
      const result = await agentRef.current.analyze(question);
      setAnalysis(result);
      setConversationHistory([...conversationHistory, result]);
      setQuestion('');

      // Scroll to results
      setTimeout(() => {
        scrollRef.current?.scrollIntoView({ behavior: 'smooth' });
      }, 100);
    } catch (error) {
      setAnalysis({
        question,
        sql: '',
        results: [],
        interpretation: '',
        visualization: null,
        timestamp: new Date(),
        status: 'error',
        error: error instanceof Error ? error.message : 'An error occurred',
      });
    } finally {
      setLoading(false);
    }
  };

  const handleSampleQuestion = (sampleQuestion: string) => {
    setQuestion(sampleQuestion);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900">
      {/* Header */}
      <header className="sticky top-0 z-50 border-b border-slate-700 bg-slate-900/80 backdrop-blur-xl">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex items-center gap-3">
            <div className="flex items-center justify-center h-10 w-10 rounded-lg bg-gradient-to-br from-blue-500 to-cyan-500 shadow-lg">
              <Database className="h-6 w-6 text-white" />
            </div>
            <div>
              <h1 className="text-2xl font-bold text-white">Data Analyst Agent</h1>
              <p className="text-sm text-slate-400">Ask questions about your data in natural language</p>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Query Input Section */}
        <div className="mb-8">
          <form onSubmit={handleSubmit} className="space-y-4">
            <div className="relative">
              <input
                type="text"
                value={question}
                onChange={(e) => setQuestion(e.target.value)}
                placeholder="Ask a question about your data (e.g., 'What were total sales by category?')"
                className="w-full px-4 py-3 bg-slate-800 border border-slate-600 rounded-lg text-white placeholder-slate-400 focus:outline-none focus:border-blue-500 focus:ring-2 focus:ring-blue-500/20 transition-all"
                disabled={loading}
              />
              <button
                type="submit"
                disabled={loading || !question.trim()}
                className="absolute right-2 top-1/2 -translate-y-1/2 p-2 bg-gradient-to-r from-blue-500 to-cyan-500 text-white rounded-lg hover:shadow-lg hover:shadow-blue-500/50 disabled:opacity-50 disabled:cursor-not-allowed transition-all"
              >
                {loading ? (
                  <Loader className="h-5 w-5 animate-spin" />
                ) : (
                  <Send className="h-5 w-5" />
                )}
              </button>
            </div>

            {/* Sample Questions */}
            {!analysis && <SampleQuestions onSelectQuestion={handleSampleQuestion} />}
          </form>
        </div>

        {/* Results Section */}
        {analysis && (
          <div ref={scrollRef} className="space-y-6">
            {analysis.status === 'error' ? (
              <div className="bg-red-500/10 border border-red-500/30 rounded-lg p-4 flex gap-3">
                <AlertCircle className="h-5 w-5 text-red-400 flex-shrink-0 mt-0.5" />
                <div>
                  <h3 className="text-red-300 font-semibold mb-1">Error Processing Query</h3>
                  <p className="text-red-200 text-sm">{analysis.error}</p>
                </div>
              </div>
            ) : (
              <>
                {/* Query Preview */}
                <QueryPreview
                  question={analysis.question}
                  sql={analysis.sql}
                  onToggle={setShowPreview}
                  isExpanded={showPreview}
                />

                {/* Results Display */}
                <ResultsDisplay
                  results={analysis.results}
                  visualization={analysis.visualization}
                  interpretation={analysis.interpretation}
                />

                {/* Follow-up Action */}
                <div className="bg-slate-800 border border-slate-700 rounded-lg p-4 flex items-start gap-3">
                  <TrendingUp className="h-5 w-5 text-cyan-400 flex-shrink-0 mt-0.5" />
                  <div>
                    <h3 className="text-white font-semibold mb-2">Next Steps</h3>
                    <p className="text-slate-300 text-sm mb-3">
                      Ask a follow-up question to drill deeper into the data, compare metrics, or explore different time periods.
                    </p>
                    <button
                      onClick={() => setQuestion('')}
                      className="text-sm px-3 py-1 bg-slate-700 hover:bg-slate-600 text-cyan-400 rounded transition-colors"
                    >
                      Ask Another Question
                    </button>
                  </div>
                </div>
              </>
            )}
          </div>
        )}

        {/* Conversation History */}
        {conversationHistory.length > 1 && (
          <div className="mt-12 pt-8 border-t border-slate-700">
            <h2 className="text-xl font-bold text-white mb-4">Conversation History</h2>
            <div className="space-y-3">
              {conversationHistory.slice(0, -1).map((item, idx) => (
                <div
                  key={idx}
                  className="bg-slate-800 border border-slate-700 rounded-lg p-3 cursor-pointer hover:border-slate-600 transition-colors"
                  onClick={() => setAnalysis(item)}
                >
                  <p className="text-white text-sm font-medium">{item.question}</p>
                  <p className="text-slate-400 text-xs mt-1">
                    {new Date(item.timestamp).toLocaleTimeString()}
                  </p>
                </div>
              ))}
            </div>
          </div>
        )}
      </main>
    </div>
  );
}