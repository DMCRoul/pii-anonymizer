from loader import load_text_file
from detector import detect_all
from anonymizer import anonymize_text
from writer import save_anonymized_text, save_replacements_csv


def main():
    file_path = "data/sample.txt"

    try:
        text = load_text_file(file_path)

        print("=== Исходный текст ===\n")
        print(text)

        entities = detect_all(text)

        print("\n=== Найденные сущности ===")
        for entity in entities:
            print(entity)

        anonymized_text, replacements = anonymize_text(text, entities)

        print("\n=== Анонимизированный текст ===\n")
        print(anonymized_text)

        print("\n=== Замены ===")
        for replacement in replacements:
            print(replacement)

        saved_text_path = save_anonymized_text(anonymized_text)
        saved_csv_path = save_replacements_csv(replacements)

        print("\n=== Файлы сохранены ===")
        print("Текст:", saved_text_path)
        print("CSV:", saved_csv_path)

    except Exception as e:
        print("Ошибка:", e)


if __name__ == "__main__":
    main()