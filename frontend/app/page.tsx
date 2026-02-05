'use client';

import { useState } from 'react';
import dynamic from 'next/dynamic';
import { useEngineStore } from '@/lib/store';
import Console from './components/Console';
import DiffViewer from './components/DiffViewer';
import LibraryBadges from './components/LibraryBadges';

// Dynamic import for Monaco (SSR not supported)
const CodeEditor = dynamic(() => import('./components/CodeEditor'), {
  ssr: false,
  loading: () => <div className="h-[400px] bg-gray-800 animate-pulse rounded-lg" />,
});

export default function Home() {
  const { code, setCode, errorLog, setErrorLog, logs, appendLog, clearLogs, isLoading, setLoading, result, setResult } = useEngineStore();
  const [showDiff, setShowDiff] = useState(false);
  const [fixedCode, setFixedCode] = useState('');

  const handleSubmit = async () => {
    if (!code.trim() || !errorLog.trim()) {
      alert('Please enter both code and error log.');
      return;
    }

    setLoading(true);
    clearLogs();
    setResult(null);
    setShowDiff(false);

    // Simulate execution (In production, this would be a WebSocket connection)
    appendLog('Connecting to Truth Engine...');

    try {
      // For demo, we'll call a local API or simulate
      appendLog('Analyzing code structure...');
      await new Promise((r) => setTimeout(r, 500));

      appendLog('Categorizing error type...');
      await new Promise((r) => setTimeout(r, 500));

      appendLog('Generating fix candidates with Gemini...');
      await new Promise((r) => setTimeout(r, 1000));

      appendLog('Running Candidate 1... [PASS]');
      await new Promise((r) => setTimeout(r, 300));

      appendLog('Running Candidate 2... [FAIL - Still errors]');
      await new Promise((r) => setTimeout(r, 300));

      appendLog('Verification complete!');

      // Mock result
      const mockFix = code.replace(/\/\s*len\(.*?\)/, ' / max(len(numbers), 1)');
      setFixedCode(mockFix);
      setResult({
        status: 'success',
        source: 'Gemini 1.5 Flash',
        errorType: 'RUNTIME',
        candidates: [mockFix],
        winner: mockFix,
      });
      setShowDiff(true);
    } catch (err) {
      appendLog('Error: Failed to connect to engine.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 via-gray-800 to-gray-900 text-white">
      {/* Header */}
      <header className="border-b border-gray-700 bg-gray-900/50 backdrop-blur-sm sticky top-0 z-10">
        <div className="max-w-7xl mx-auto px-6 py-4 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 bg-gradient-to-br from-blue-500 to-purple-600 rounded-lg flex items-center justify-center font-bold text-lg">
              TE
            </div>
            <div>
              <h1 className="text-xl font-bold">Truth Engine</h1>
              <p className="text-xs text-gray-400">Zero-Trust Python Debugger</p>
            </div>
          </div>
          <div className="flex items-center gap-4">
            <span className="px-3 py-1 rounded-full bg-green-900/50 text-green-400 text-sm border border-green-700">
              ● Connected
            </span>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-6 py-8">
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {/* Left Panel: Input */}
          <div className="space-y-6">
            <div>
              <div className="flex items-center justify-between mb-2">
                <label className="text-sm font-medium text-gray-300">
                  Your Broken Code
                </label>
                <LibraryBadges code={code} />
              </div>
              <CodeEditor
                value={code}
                onChange={setCode}
                height="300px"
              />
            </div>

            <div>
              <label className="text-sm font-medium text-gray-300 block mb-2">
                Error Log / Traceback
              </label>
              <textarea
                value={errorLog}
                onChange={(e) => setErrorLog(e.target.value)}
                placeholder="Paste your error traceback here..."
                className="w-full h-32 bg-gray-800 border border-gray-700 rounded-lg p-3 text-sm font-mono text-red-400 placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
            </div>

            <button
              onClick={handleSubmit}
              disabled={isLoading}
              className={`w-full py-3 rounded-lg font-semibold text-lg transition-all ${isLoading
                  ? 'bg-gray-700 cursor-not-allowed'
                  : 'bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-500 hover:to-purple-500 shadow-lg hover:shadow-blue-500/25'
                }`}
            >
              {isLoading ? 'Verifying...' : '🚀 Verify & Fix'}
            </button>
          </div>

          {/* Right Panel: Output */}
          <div className="space-y-6">
            <Console />

            {showDiff && result && (
              <div className="space-y-4">
                <div className="flex items-center justify-between">
                  <h3 className="text-lg font-semibold text-green-400">
                    ✓ Verified Fix Found
                  </h3>
                  <span className="text-sm text-gray-400">
                    Source: {result.source}
                  </span>
                </div>
                <DiffViewer original={code} modified={fixedCode} />
                <button
                  onClick={() => {
                    navigator.clipboard.writeText(fixedCode);
                    alert('Fixed code copied to clipboard!');
                  }}
                  className="w-full py-2 rounded-lg bg-green-700 hover:bg-green-600 transition-colors font-medium"
                >
                  📋 Copy Fixed Code
                </button>
              </div>
            )}
          </div>
        </div>
      </main>
    </div>
  );
}
