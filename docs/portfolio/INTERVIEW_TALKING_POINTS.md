# Interview Talking Points

## Project Summary

I built an AI-powered Finance and Supply Chain Copilot that combines market data, financial document retrieval, LLM-generated analysis, alerting, and supply chain risk extraction into a Streamlit business intelligence dashboard.

## Product Framing

The product helps analysts and managers answer questions such as:

- What changed in a company's financial position?
- What risks are disclosed in annual reports?
- Are there supply chain risks buried in filings?
- Should a stock or company be monitored more closely?

## Architecture Explanation

The system separates UI, data ingestion, RAG, memory, tools, alerts, and LLM orchestration. This keeps the app easy to extend and makes the codebase readable for recruiters and technical reviewers.

## Resume Bullets

- Designed and built a modular AI copilot for finance and supply chain decision support using Streamlit, Groq, LangChain, ChromaDB, and open-source embeddings.
- Implemented a RAG architecture for annual report analysis, including PDF ingestion, semantic search, grounded question answering, and source citation design.
- Built finance workflows for stock lookup, price history, KPI extraction design, AI-generated investment insights, and alert evaluation.
- Created an extensible tool-calling architecture that can evolve into agentic workflows, MCP-compatible tools, or multi-agent orchestration.
- Documented architecture, deployment, business use cases, tradeoffs, and learning outcomes for a recruiter-friendly AI engineering portfolio.

## Tradeoffs to Explain

- I used Streamlit first because it lets me build a complete product quickly while learning AI engineering.
- I chose ChromaDB and sentence-transformers because they are free, local, and reproducible.
- I kept model settings in environment variables so the app can adapt as model availability changes.
- I started with session memory because it is simple, then designed a path to SQLite for longer-term memory.
