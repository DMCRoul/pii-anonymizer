from pathlib import Path


def load_text_file(file_path: str) -> str:
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError("Файл не найден")

    text = path.read_text(encoding="utf-8")

    return text