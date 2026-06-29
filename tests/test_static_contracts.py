import ast
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
APP = ROOT / "app.py"
PROD = ROOT / "app_production.py"
README = ROOT / "readme.md"
REPORT_TEMPLATE = ROOT / "templates" / "report.html"
UPLOAD_TEMPLATE = ROOT / "templates" / "upload.html"
GITIGNORE = ROOT / ".gitignore"


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def route_paths(source: str) -> set[str]:
    tree = ast.parse(source)
    routes: set[str] = set()
    for node in ast.walk(tree):
        if not isinstance(node, ast.FunctionDef):
            continue
        for dec in node.decorator_list:
            if isinstance(dec, ast.Call) and isinstance(dec.func, ast.Attribute):
                if dec.func.attr == "route" and dec.args and isinstance(dec.args[0], ast.Constant):
                    routes.add(str(dec.args[0].value))
    return routes


def test_public_route_contract_is_stable():
    expected = {"/", "/triage", "/upload", "/er", "/schedule", "/confirmation", "/report", "/about", "/contact"}
    assert expected.issubset(route_paths(read(APP)))
    assert expected.issubset(route_paths(read(PROD)))


def test_production_entrypoint_does_not_enable_debug_mode():
    source = read(PROD)
    assert "debug=True" not in source
    assert "debug=False" in source


def test_medical_disclaimer_language_is_present():
    combined = "\n".join(read(p) for p in [README, REPORT_TEMPLATE])
    lowered = combined.lower()
    assert "not medical advice" in lowered or "informational purposes only" in lowered
    assert "clinical validation required" in lowered or "professional medical" in lowered


def test_upload_flow_restricts_file_extensions_and_uses_secure_filename():
    source = read(APP) + "\n" + read(PROD)
    assert "secure_filename" in source
    assert "ALLOWED_EXTENSIONS" in read(APP)
    assert "png" in source and "jpg" in source and "jpeg" in source


def test_runtime_sensitive_files_are_ignored_by_git():
    ignore = read(GITIGNORE)
    required_patterns = [".env", "uploads", "*.pth", "*.zip"]
    missing = [pattern for pattern in required_patterns if pattern not in ignore]
    assert not missing, f"Missing runtime-sensitive ignore patterns: {missing}"
