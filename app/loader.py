from pathlib import Path
import pandas as pd


def load_text_file(file_path: str) -> str:
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError("Файл не найден")

    text = path.read_text(encoding="utf-8")

    return text


def load_csv_file(file_path: str) -> pd.DataFrame:
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError("CSV файл не найден")

    df = pd.read_csv(path)

    if df.empty:
        raise ValueError("CSV файл пустой")

    return df