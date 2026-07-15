# XAU Dynamics - MacroAI Sentiment Engine 🧠📊

The core intelligence layer of the XAU Dynamics architectural stack. **MacroAI** is an advanced, asynchronous Natural Language Processing (NLP) microservice that leverages Large Language Models (LLMs) to perform ultra-fast sentiment analysis on macroeconomic data releases and central bank statements.

## 🎯 Strategic Objective

While traditional algorithms react to price action *after* a macroeconomic event, **MacroAI** parses raw economic text (e.g., FOMC statements, NFP data) in real-time. It computes an institutional-grade sentiment score and immediately forwards strict execution directives to the `TradeBridge API`, preventing the MT5 execution layer from entering low-liquidity institutional traps.

## ⚙️ Architecture & Azure Integration

This microservice is heavily optimized for cloud deployment, specifically architected to leverage **Microsoft Azure OpenAI Services** (GPT-4 Turbo) for secure, high-throughput, and sub-second latency inference.

*   **Ingestion:** Receives raw WebSocket feeds from the `NewsGuard` microservice.
*   **Inference:** Asynchronous LLM processing using strict `Pydantic` JSON schemas to ensure deterministic outputs.
*   **Output:** Pushes calculated risk-adjusted signals to `TradeBridge` via RESTful POST requests.

## 🚀 Enterprise Features

- **Real-Time NLP Analysis:** Instantly interprets complex central bank rhetoric (Hawkish vs. Dovish).
- **Deterministic JSON Generation:** Forces the LLM to output machine-readable JSON formats directly consumable by algorithmic trading bots.
- **Fail-Safe Mode:** If API latency exceeds 500ms during a high-impact news event, the engine automatically issues a `HALT_TRADING` directive to protect capital.
- **Vector Ready:** Architecture prepared for RAG (Retrieval-Augmented Generation) using Azure Cosmos DB to compare current economic data against historical market reactions.

## 🛠️ Tech Stack & Dependencies

*   **Core:** Python 3.11+
*   **AI/LLM:** OpenAI Async API / Azure OpenAI SDK
*   **Validation:** Pydantic V2
*   **Networking:** Aiohttp, Asyncio
