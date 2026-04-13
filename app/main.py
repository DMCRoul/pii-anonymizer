from loader import load_text_file
from detector import detect_all


def main():
    file_path = "data/sample.txt"

    try:
        text = load_text_file(file_path)

        print("Файл загружен успешно\n")
        print("=== Содержимое ===")
        print(text)

        entities = detect_all(text)

        print("\n=== Найденные сущности ===")
        for entity in entities:
            print(entity)

    except Exception as e:
        print("Ошибка:", e)


if __name__ == "__main__":
    main()