import { useState } from 'react';

const API_BASE = 'http://localhost:8000/api';

export function usePlayground() {
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<any>(null);
  const [error, setError] = useState<string | null>(null);

  const [evalLoading, setEvalLoading] = useState(false);
  const [evalResults, setEvalResults] = useState<any>(null);

  const runExtraction = async (strategy: string, modelId: string, text: string) => {
    setLoading(true);
    setResult(null);
    setError(null);
    try {
      const res = await fetch(`${API_BASE}/execute`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ workflow_strategy: strategy, model_id: modelId, input_text: text })
      });
      if (!res.ok) {
        const d = await res.json();
        throw new Error(d.detail || `HTTP error! status: ${res.status}`);
      }
      const data = await res.json();
      setResult(data.result);
    } catch (e: any) {
      setError(e.message);
    } finally {
      setLoading(false);
    }
  };

  const runEvaluation = async (strategy: string, modelId: string) => {
    setEvalLoading(true);
    setEvalResults(null);
    try {
      const res = await fetch(`${API_BASE}/evaluate`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ workflow_strategy: strategy, model_id: modelId })
      });
      if (!res.ok) {
         const d = await res.json();
         throw new Error(d.detail || `HTTP error! status: ${res.status}`);
      }
      const data = await res.json();
      setEvalResults(data);
    } catch (e: any) {
      console.error(e);
    } finally {
      setEvalLoading(false);
    }
  };

  return { runExtraction, result, loading, error, runEvaluation, evalResults, evalLoading };
}
