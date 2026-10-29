from pathlib import Path
from pypdf import PdfReader


def extract_resume_text(file_path: str | Path) -> str:
    """Extract text from a PDF resume."""
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"Resume not found: {path}")

    if path.suffix.lower() != ".pdf":
        raise ValueError("Please provide a PDF resume.")

    reader = PdfReader(str(path))

    text = "\n".join(
        page.extract_text() or ""
        for page in reader.pages
    ).strip()

    if not text:
        raise ValueError(
            "No readable text found. The PDF may be scanned."
        )

    return text
