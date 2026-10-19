from app import safe_search

def test_search_finds_known_source():
    results = safe_search("FastAPI")
    assert any(item["path"] == "app.py" for item in results)

def test_search_no_match_returns_empty():
    assert safe_search("unlikely-token-987654") == []
