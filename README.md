# 🧪 LLM Evaluation Playground

A professional-grade, full-stack platform designed to systematically evaluate, compare, and benchmark Large Language Model (LLM) extraction workflows.

## 📖 Overview

As AI adoption shifts from conversational chatbots to deterministic backend processes, one of the biggest challenges for engineering teams is ensuring **reliability**. Prompt engineering is no longer enough; teams need scientifically backed comparatives before deploying an LLM into production.

The **LLM Evaluation Playground** solves this by providing a controlled environment (a "Playground") where different AI Models (Open Source vs Proprietary) and Prompting Strategies (Baseline vs Strict vs Tool Calling) are pitted against each other over a Golden Dataset, automatically graded by predefined analytical evaluators.

## 💼 Business Value (Product Owner Perspective)

*   **Data-Driven AI Decisions:** Removes guesswork from AI implementation. Instead of assessing models through trial and error, it provides mathematical accuracy scores (`Exact Match`, `Field Coverage`, `Format Validity`).
*   **Cost vs Performance Analysis:** Allows teams to test if a cheaper, smaller model (e.g., Llama 3 8B) can achieve the same extraction accuracy as a heavy standard model (e.g., Gemini Pro) for a specific workflow.
*   **Production Readiness Validation:** Ensures that the required AI pipeline has a 100% stable schema return rate (Zero-hallucination structured outputs) before connecting it to a live database or ERP.

## 🛠️ Technical Architecture

This application is decoupled into a robust Python Backend engine and a modern React Frontend, operating as a Monorepo.

### Backend (Python)
*   **Core:** FastAPI & Pydantic. Serves as a high-concurrency orchestrator utilizing Uvicorn (ASGI).
*   **LLM Engine:** Implements a dynamic *Factory Pattern* for seamless dependency injection of various LLM Providers (Google GenAI & Meta Llama via Groq).
*   **Orchestration:** Leverages **LangChain** for Workflow execution and Tool Calling binding.
*   **Observability:** Fully integrated with **LangSmith** for deep tracing, latencies, and token cost tracking.

### Frontend (TypeScript)
*   **Core:** React 19, Vite, & TailwindCSS v4.
*   **UX/UI:** Provides a sleek, premium, "dark-modern" dashboard interface.
*   **State Management:** Separates concerns into a single-pass `Playground` for manual data testing, and an `Evaluations` dashboard for massive batch-run analytics using custom hooks (`usePlayground.ts`).

## 🏗️ Execution Strategies (Workflows)

The engine currently benchmarks three distinct abstraction levels for data extraction:
1.  **Baseline Extraction:** A loose, generic zero-shot prompt. Fast, but volatile.
2.  **Strict Prompting:** A highly-constrained "Chain of Thought" prompt enforcing JSON-mode.
3.  **Structured Output (Tool Calling):** The zenith of reliability; utilizes Native Tool Calling on the LLM core to strictly bind outputs against a predefined Pydantic Schema. 

---

## 🚀 Getting Started (Local Deployment)

### Prerequisites
* Python 3.11+
* Node.js 18+
* Developer API Keys (Groq, Google AI Studio, and optionally LangChain)

### 1. Environment Setup
At the root of the project, duplicate the environment template and fill in your keys:
```bash
cp .env.example .env
```

### 2. Backend Initialization
Open a terminal in the root directory:
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r backend/requirements.txt
```

Launch the API server (Runs on port 8000 by default):
```bash
cd backend
uvicorn app.main:app --reload
```

### 3. Frontend Initialization
Open a new terminal window:
```bash
cd frontend
npm install
npm run dev
```

Visit the application loaded at `http://localhost:5173`. Select your AI provider and workflow, and start benchmarking!
