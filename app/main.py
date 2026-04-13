from loader import load_text_file, load_csv_file
from detector import detect_all
from anonymizer import anonymize_text
from writer import (
    save_anonymized_text,
    save_replacements_csv,
    save_dataframe_csv,
)


def process_txt():
    file_path = "data/sample.txt"

    text = load_text_file(file_path)

    print("=== Исходный TXT ===\n")
    print(text)

    entities = detect_all(text)

    print("\n=== Найденные сущности ===")
    for entity in entities:
        print(entity)

    anonymized_text, replacements = anonymize_text(text, entities)

    print("\n=== Анонимизированный TXT ===\n")
    print(anonymized_text)

    save_anonymized_text(anonymized_text)
    save_replacements_csv(replacements)

    print("\nTXT обработан и сохранён в output/")


def process_csv():
    file_path = "data/sample.csv"

    df = load_csv_file(file_path)

    if "text" not in df.columns:
        raise ValueError("В CSV нет колонки 'text'")

    anonymized_texts = []

    for text in df["text"]:
        text = str(text)
        entities = detect_all(text)
        anonymized_text, _ = anonymize_text(text, entities)
        anonymized_texts.append(anonymized_text)

    df["anonymized_text"] = anonymized_texts

    saved_csv_path = save_dataframe_csv(df)

    print("\n=== CSV обработан ===")
    print(df)
    print(f"\nФайл сохранён: {saved_csv_path}")


def main():
    try:
        process_txt()
        process_csv()

    except Exception as e:
        print("Ошибка:", e)


if __name__ == "__main__":
    main()