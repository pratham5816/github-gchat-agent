GitHub GChat Agent

GitHub GChat Agent is an autonomous AI developer assistant designed to seamlessly bridge GitHub repository management with Google Chat collaboration workflows. Built with FastAPI and LangChain, it empowers engineering teams to query repository activity, track open issues, inspect pull requests, and broadcast automated summaries directly into Google Chat spaces using natural language.

Why GitHub GChat Agent?

Developer visibility often gets fragmented across disjointed browser tabs, issue trackers, and chat channels. This project centralizes team awareness by deploying an intelligent agent that parses developer prompts, automates repository audits, and posts structured updates directly where team discussions happen.

Key Features
Dual-Engine LLM Support: Switch flexibly between Google Gemini (gemini-3.5-flash-lite) for fast cloud reasoning and Ollama (llama3.2:3b) for private, local, zero-cost inference.
GitHub Tool Integrations: Purpose-built LangChain tools interact directly with the GitHub REST API to inspect repository states, filter open/closed issues, and summarize active pull requests with rich metadata (authors, branches, URLs, and descriptions).
Google Chat Integration: Features a full OAuth 2.0 flow with automatic token expiration checks and background token refreshes to ensure uninterrupted automated posting to target spaces.
High-Performance FastAPI Architecture: Pre-warms agent instances during application lifespan startup to eliminate cold-start overhead, exposing both unified and model-specific REST endpoints backed by strict Pydantic schema validation.
Modular & Extensible: Clean separation of agent definitions, API tools, and integrations, making it straightforward to add CI/CD pipeline triggers, release alerts, or additional communication channels.
Tech Stack

Python 3.12+ • FastAPI • LangChain • Google Gemini API • Ollama • Uvicorn • GitHub REST API • Google Workspace Chat API
