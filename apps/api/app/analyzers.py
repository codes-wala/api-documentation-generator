import ast
import json
from pathlib import PurePath

ALLOWED_EXTENSIONS = {".json", ".py", ".js", ".ts", ".yaml", ".yml"}

def analyze_source(filename: str, content: str) -> dict:
    suffix = PurePath(filename).suffix.lower()
    if suffix == ".json":
        try: data = json.loads(content)
        except json.JSONDecodeError as exc: raise ValueError(f"Invalid JSON at line {exc.lineno}, column {exc.colno}.") from exc
        return {"kind": "json", "root_type": type(data).__name__, "structure": describe_json(data), "notes": ["JSON examples do not prove an endpoint URL or HTTP method."]}
    if suffix == ".py":
        try: tree = ast.parse(content)
        except SyntaxError as exc: raise ValueError(f"Python syntax error at line {exc.lineno}: {exc.msg}") from exc
        functions, classes = [], []
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                functions.append({"name": node.name, "async": isinstance(node, ast.AsyncFunctionDef), "parameters": [a.arg for a in node.args.args], "returns": ast.unparse(node.returns) if node.returns else None, "docstring": ast.get_docstring(node)})
            elif isinstance(node, ast.ClassDef): classes.append({"name": node.name, "docstring": ast.get_docstring(node)})
        return {"kind": "python", "functions": functions, "classes": classes, "notes": ["Static analysis only; source code was not executed."]}
    if suffix in {".js", ".ts"}:
        import re
        functions = re.findall(r"(?:async\s+)?function\s+([A-Za-z_$][\w$]*)\s*\(([^)]*)\)", content)
        arrows = re.findall(r"(?:const|let|var)\s+([A-Za-z_$][\w$]*)\s*=\s*(?:async\s*)?\(([^)]*)\)\s*=>", content)
        return {"kind": "javascript" if suffix == ".js" else "typescript", "functions": [{"name": n, "parameters": [p.strip() for p in args.split(",") if p.strip()]} for n, args in functions + arrows], "analysis_level": "partial pattern analysis", "notes": ["Use an AST parser for more complete language analysis; declarations outside recognized patterns may be missed."]}
    if suffix in {".yaml", ".yml"}:
        return {"kind": "yaml", "analysis_level": "not parsed", "notes": ["YAML is accepted as text in this initial release but is not yet semantically parsed. Use JSON OpenAPI input where possible."]}
    raise ValueError("Unsupported file type. Supported extensions: .json, .py, .js, .ts, .yaml, .yml.")

def describe_json(value, depth=0):
    if depth > 6: return {"type": "nested", "note": "depth limit reached"}
    if isinstance(value, dict): return {"type": "object", "properties": {str(k): describe_json(v, depth + 1) for k, v in list(value.items())[:200]}}
    if isinstance(value, list): return {"type": "array", "items": describe_json(value[0], depth + 1) if value else {"type": "unknown"}, "example_count": len(value)}
    if value is None: kind = "null"
    elif isinstance(value, bool): kind = "boolean"
    elif isinstance(value, int): kind = "integer"
    elif isinstance(value, float): kind = "number"
    else: kind = "string"
    return {"type": kind, "example": value if isinstance(value, (str, int, float, bool)) or value is None else None}
