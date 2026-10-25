from app.pdf_exporter import markdown_to_pdf

def test_pdf_export_returns_pdf_bytes():
    result = markdown_to_pdf("Example API", "# Overview\n\nA short description.\n\n```python\ndef ping():\n    return True\n```")
    assert result.startswith(b"%PDF-")
    assert len(result) > 500
