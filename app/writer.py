from pathlib import Path
import csv
import json


OUTPUT_DIR = Path("output")


def ensure_output_dir():
    OUTPUT_DIR.mkdir(exist_ok=True)


def save_anonymized_text(text, filename="anonymized.txt"):
    ensure_output_dir()
    file_path = OUTPUT_DIR / filename
    file_path.write_text(text, encoding="utf-8")
    return file_path


def save_replacements_csv(replacements, filename="replacements.csv"):
    ensure_output_dir()
    file_path = OUTPUT_DIR / filename

    with file_path.open("w", newline="", encoding="utf-8") as csvfile:
        fieldnames = ["original", "replacement", "type"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        writer.writerows(replacements)

    return file_path


def save_dataframe_csv(df, filename="anonymized_data.csv"):
    ensure_output_dir()
    file_path = OUTPUT_DIR / filename
    df.to_csv(file_path, index=False, encoding="utf-8")
    return file_path


def save_summary(summary, filename="dataset_summary.json"):
    ensure_output_dir()
    file_path = OUTPUT_DIR / filename

    with file_path.open("w", encoding="utf-8") as f:
        json.dump(summary, f, indent=4)

    return file_path