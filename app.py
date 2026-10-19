from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from pathlib import Path

app = FastAPI(title="MCP AI Developer Assistant", version="0.1.0")
ROOT = Path(__file__).parent.resolve()
ALLOWED = {".py", ".md", ".ts", ".tsx", ".js", ".json", ".yml", ".yaml", ".toml"}

class SearchRequest(BaseModel):
    query: str = Field(min_length=1)
    max_results: int = Field(default=10, ge=1, le=50)

def safe_search(query: str, max_results: int = 10) -> list[dict]:
    results = []
    needle = query.lower()
    for path in sorted(ROOT.rglob("*")):
        if not path.is_file() or path.suffix not in ALLOWED or any(p in {".git", ".venv", "__pycache__"} for p in path.parts):
            continue
        try:
            for line_no, line in enumerate(path.read_text(encoding="utf-8", errors="ignore").splitlines(), 1):
                if needle in line.lower():
                    results.append({"path":str(path.relative_to(ROOT)), "line":line_no, "text":line.strip()[:240]})
                    if len(results) >= max_results: return results
        except OSError:
            continue
    return results

@app.get("/health")
def health(): return {"status":"ok"}

@app.get("/tools")
def tools():
    return {"tools":[{"name":"search_repository","description":"Read-only case-insensitive search in allowlisted text files"},
                     {"name":"repository_summary","description":"Counts files by extension; does not execute code"}]}

@app.post("/tools/search")
def search(request: SearchRequest):
    return {"query":request.query, "results":safe_search(request.query, request.max_results), "read_only":True}

@app.get("/tools/summary")
def summary():
    counts = {}
    for path in ROOT.rglob("*"):
        if path.is_file() and not any(p in {".git", ".venv", "__pycache__"} for p in path.parts):
            key = path.suffix or "[no extension]"
            counts[key] = counts.get(key, 0) + 1
    return {"file_count":sum(counts.values()), "by_extension":counts, "read_only":True}
