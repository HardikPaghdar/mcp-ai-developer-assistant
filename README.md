# MCP AI Developer Assistant

A safe local developer-tool surface for repository inspection. The current implementation exposes read-only tools over HTTP; it is not yet an MCP-protocol server.

## Features
- Search allowlisted source/document files with line references
- Repository file-count summary by extension
- Bounded results and truncated matching lines
- Explicit read-only tool descriptions
- Automated tests and CI

## Run
```bash
pip install -r requirements.txt
uvicorn app:app --reload
```
API docs: http://127.0.0.1:8000/docs.

## Safety model
Only selected text-file extensions are searched. Results are read-only and bounded. The prototype does not execute commands or write files. Add the official MCP SDK adapter as a separate transport layer and keep tool permissions explicit.

## Stack
Python, FastAPI, Pydantic, pytest. Free/open-source dependencies.

## Explore more

- [MCP Server Developer Toolkit](https://github.com/HardikPaghdar/mcp-server-developer-toolkit) — permission-aware AI client tools.
- [Codebase RAG AI Developer](https://github.com/HardikPaghdar/codebase-rag-ai-developer) — local-first codebase retrieval.
- [LLM Security & Prompt Injection Testing Lab](https://github.com/HardikPaghdar/llm-security-prompt-injection-lab) — tool permission regression tests.
- [More projects on my portfolio](https://hardikpaghdar.netlify.app/).
