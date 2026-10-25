import pytest
from app.analyzers import analyze_source

def test_json_analyzer_describes_nested_shape():
    result = analyze_source("response.json", '{"city":"Tokyo","temperature":22.5,"ok":true}')
    assert result["kind"] == "json"
    assert result["structure"]["type"] == "object"
    assert result["structure"]["properties"]["city"]["type"] == "string"
    assert result["structure"]["properties"]["temperature"]["type"] == "number"

def test_invalid_json_is_rejected():
    with pytest.raises(ValueError, match="Invalid JSON"):
        analyze_source("bad.json", '{"x":')

def test_python_source_is_parsed_not_executed():
    result = analyze_source("example.py", 'def get_weather(city: str) -> dict:\n    """Get weather."""\n    return {}\n')
    assert result["kind"] == "python"
    assert result["functions"][0]["name"] == "get_weather"
    assert result["functions"][0]["returns"] == "dict"

def test_unsupported_extension_rejected():
    with pytest.raises(ValueError, match="Unsupported file type"):
        analyze_source("program.exe", "not safe")
