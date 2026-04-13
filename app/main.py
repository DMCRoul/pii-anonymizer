from loader import load_text_file
from detector import detect_all
from anonymizer import anonymize_text


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
        for r in replacements:
            print(r)

    except Exception as e:
        print("Ошибка:", e)


if __name__ == "__main__":
    main()