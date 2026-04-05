import { Activity, TestTube2, GitCompare, Code2, Send, Loader2, CheckCircle2, XCircle } from 'lucide-react';
import { useState } from 'react';
import { usePlayground } from './hooks/usePlayground';

function App() {
  const [activeTab, setActiveTab] = useState('playground'); 
  const [strategy, setStrategy] = useState('structured');
  const [modelId, setModelId] = useState('llama-3.1-8b-instant');
  const [text, setText] = useState('');
  
  const { runExtraction, result, loading, error, runEvaluation, evalResults, evalLoading } = usePlayground();

  const handleRun = () => {
    if (!text) return;
    runExtraction(strategy, modelId, text);
  };

  return (
    <div className="min-h-screen bg-slate-900 text-slate-100 flex flex-col font-sans">
      <header className="border-b border-slate-800 bg-slate-950/50 backdrop-blur-md sticky top-0 z-10">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
          <div className="flex items-center gap-3 text-blue-500">
            <TestTube2 className="h-6 w-6" />
            <h1 className="text-xl font-semibold text-slate-100 hidden sm:block tracking-tight">
              LLM Evaluation Playground
            </h1>
          </div>
          
          <nav className="flex space-x-1 sm:space-x-4">
            <button 
              onClick={() => setActiveTab('playground')}
              className={`px-4 py-2 rounded-md transition-colors text-sm font-medium ${activeTab === 'playground' ? 'bg-blue-600/10 text-blue-400' : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800'}`}
            >
              Playground
            </button>
            <button 
              onClick={() => setActiveTab('evaluations')}
              className={`px-4 py-2 rounded-md transition-colors text-sm font-medium ${activeTab === 'evaluations' ? 'bg-blue-600/10 text-blue-400' : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800'}`}
            >
              Evaluations
            </button>
            <a href="https://github.com" target="_blank" rel="noreferrer" className="flex items-center ml-2 text-slate-400 hover:text-slate-200 transition-colors">
              <Code2 className="w-5 h-5 mx-2" />
            </a>
          </nav>
        </div>
      </header>

      <main className="flex-1 max-w-7xl mx-auto w-full px-4 sm:px-6 lg:px-8 py-8">
        
        {activeTab === 'playground' && (
           <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 h-[calc(100vh-120px)]">
              <div className="flex flex-col gap-6">
                
                <div className="bg-slate-800/50 border border-slate-700/50 rounded-xl p-5 shadow-sm shrink-0">
                  <h2 className="text-sm font-semibold text-slate-300 uppercase tracking-wider mb-4">Configuration</h2>
                  
                  <div className="space-y-4">
                    <div>
                      <label className="block text-sm font-medium text-slate-400 mb-2">AI Provider (Model)</label>
                      <select 
                        value={modelId}
                        onChange={e => setModelId(e.target.value)}
                        className="w-full bg-slate-900 border border-slate-700 rounded-lg px-4 py-2.5 text-sm text-slate-200 focus:ring-2 focus:ring-emerald-500 focus:border-emerald-500 outline-none transition-all"
                      >
                        <option value="llama-3.1-8b-instant">Llama 3.1 8B (Groq)</option>
                        <option value="llama-3.3-70b-versatile">Llama 3.3 70B (Groq)</option>
                        <option value="gemini-2.5-flash">Gemini 2.5 Flash (Google)</option>
                        <option value="gemini-2.5-pro">Gemini 2.5 Pro (Google)</option>
                      </select>
                    </div>
                    <div>
                      <label className="block text-sm font-medium text-slate-400 mb-2">Workflow Strategy</label>
                      <select 
                        value={strategy}
                        onChange={e => setStrategy(e.target.value)}
                        className="w-full bg-slate-900 border border-slate-700 rounded-lg px-4 py-2.5 text-sm text-slate-200 focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none transition-all"
                      >
                        <option value="baseline">Baseline Extraction (Prompt Simple)</option>
                        <option value="strict">Strict Prompting (Chain of Thought)</option>
                        <option value="structured">Structured Output (Tool Calling)</option>
                      </select>
                    </div>
                  </div>
                </div>

                <div className="bg-slate-800/50 border border-slate-700/50 rounded-xl p-5 shadow-sm flex-1 flex flex-col min-h-[250px]">
                  <div className="flex items-center justify-between mb-4">
                    <h2 className="text-sm font-semibold text-slate-300 uppercase tracking-wider flex-1">Input Text</h2>
                    <button 
                      onClick={() => setText("Hey support, my account ID 10934 is locked out. I tried resetting my password but the 'Forgot Password' link on the login page gives me a 500 error. This is urgent as I need to pay my invoice today.")}
                      className="text-xs text-blue-400 hover:text-blue-300 transition-colors bg-blue-500/10 px-2 py-1 rounded"
                    >Load Example</button>
                  </div>
                  <textarea 
                    value={text}
                    onChange={e => setText(e.target.value)}
                    className="flex-1 w-full bg-slate-900 border border-slate-700 rounded-lg p-4 text-sm text-slate-300 focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none resize-none transition-all"
                    placeholder="Enter support ticket or unstructured text here..."
                  ></textarea>
                </div>

                <button 
                  onClick={handleRun}
                  disabled={loading || !text}
                  className="w-full bg-blue-600 hover:bg-blue-500 disabled:opacity-50 disabled:cursor-not-allowed text-white font-medium py-3 px-4 rounded-xl shadow-lg shadow-blue-500/25 flex justify-center items-center gap-2 transition-all active:scale-[0.98]"
                >
                  {loading ? <Loader2 className="w-4 h-4 animate-spin" /> : <Send className="w-4 h-4" />}
                  Run Extraction
                </button>
              </div>

              <div className="flex flex-col gap-6">
                
                <div className={`bg-slate-800/50 border border-slate-700/50 rounded-xl p-5 shadow-sm flex-1 flex flex-col h-full ${!result && !error ? 'opacity-50' : ''}`}>
                  <h2 className="text-sm font-semibold text-slate-300 uppercase tracking-wider mb-4 flex items-center gap-2">
                    <Activity className="w-4 h-4 text-slate-500" /> 
                    Execution Result
                  </h2>
                  <div className="flex-1 bg-slate-900/80 rounded-lg border border-slate-800 flex items-start justify-start p-4 overflow-auto">
                     {loading ? (
                         <div className="flex w-full h-full justify-center items-center"><Loader2 className="w-6 h-6 animate-spin text-blue-500" /></div>
                     ) : error ? (
                         <div className="text-red-400 text-sm whitespace-pre-wrap">{error}</div>
                     ) : result ? (
                         <pre className="text-emerald-400 text-sm font-mono whitespace-pre-wrap">{JSON.stringify(result, null, 2)}</pre>
                     ) : (
                         <div className="flex w-full h-full justify-center items-center">
                            <p className="text-slate-500 text-sm">Press "Run Extraction" to view structured output payload</p>
                         </div>
                     )}
                  </div>
                </div>

              </div>
           </div>
        )}

        {activeTab === 'evaluations' && (
           <div className="flex flex-col">
             <div className="flex flex-col items-center justify-center py-10 text-center">
               <GitCompare className="w-12 h-12 text-slate-600 mb-4" />
               <h2 className="text-xl font-semibold text-slate-200 mb-2">Evaluation Metrics</h2>
               <p className="text-slate-400 max-w-lg mb-6 text-sm">Run batch evaluations against the golden dataset. Select strategy below.</p>
               
               <div className="flex gap-4">
                  <select 
                    value={modelId}
                    onChange={e => setModelId(e.target.value)}
                    className="bg-slate-900 border border-slate-700 rounded-lg px-4 py-2 text-sm text-slate-200 focus:ring-2 focus:ring-emerald-500"
                  >
                    <option value="llama-3.1-8b-instant">Llama 3.1 8B</option>
                    <option value="llama-3.3-70b-versatile">Llama 3.3 70B</option>
                    <option value="gemini-2.5-flash">Gemini 2.5 Flash</option>
                    <option value="gemini-2.5-pro">Gemini 2.5 Pro</option>
                  </select>

                  <select 
                    value={strategy}
                    onChange={e => setStrategy(e.target.value)}
                    className="bg-slate-900 border border-slate-700 rounded-lg px-4 py-2 text-sm text-slate-200 focus:ring-2 focus:ring-blue-500"
                  >
                    <option value="baseline">Baseline</option>
                    <option value="strict">Strict Prompting</option>
                    <option value="structured">Structured Output</option>
                  </select>
                  <button 
                    onClick={() => runEvaluation(strategy, modelId)}
                    disabled={evalLoading}
                    className="bg-blue-600 hover:bg-blue-500 disabled:opacity-50 text-white font-medium py-2 px-6 flex items-center justify-center min-w-32 rounded-lg transition-colors border-0"
                  >
                     {evalLoading ? <Loader2 className="w-4 h-4 animate-spin" /> : "Start Batch"}
                  </button>
               </div>
             </div>
             
             {evalResults && (
                <div className="mt-8 border-t border-slate-800 pt-8 animate-in fade-in duration-500">
                    <h3 className="text-lg font-semibold mb-6">Aggregated Score: {strategy} ({modelId})</h3>
                    <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-10">
                        {Object.entries(evalResults.summary).map(([key, score]) => (
                            <div key={key} className="bg-slate-800/50 border border-slate-700 rounded-xl p-5 flex flex-col items-center justify-center">
                                <div className="text-sm text-slate-400 capitalize mb-2">{key.replace('_', ' ')}</div>
                                <div className="text-4xl font-bold text-emerald-400">{((score as number) * 100).toFixed(0)}%</div>
                            </div>
                        ))}
                    </div>
                    
                    <h3 className="text-lg font-semibold mb-4">Item Results</h3>
                    <div className="space-y-4">
                        {evalResults.results.map((r: any, i: number) => (
                           <div key={i} className="bg-slate-900/50 border border-slate-800 rounded-lg p-5">
                                <div className="text-sm text-slate-300 mb-3"><span className="text-slate-500 font-semibold mb-1">Input {i+1}:</span> {r.input}</div>
                                {r.error ? (
                                   <div className="text-red-400 text-sm mt-3 border-t border-red-900/30 pt-3">Error: {r.error}</div>
                                ) : (
                                   <div className="grid grid-cols-2 gap-4 mt-3 border-t border-slate-800/50 pt-3 text-xs">
                                      <div><div className="text-slate-500 mb-1">Expected</div><pre className="text-slate-400 break-all overflow-hidden">{JSON.stringify(r.expected, null, 2)}</pre></div>
                                      <div><div className="text-slate-500 mb-1">Predicted</div><pre className="text-emerald-500/80 break-all overflow-hidden">{JSON.stringify(r.prediction, null, 2)}</pre></div>
                                   </div>
                                )}
                           </div>
                        ))}
                    </div>
                </div>
             )}
           </div>
        )}

      </main>
    </div>
  )
}

export default App
