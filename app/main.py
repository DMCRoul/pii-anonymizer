from loader import load_text_file, load_csv_file
from detector import detect_all
from anonymizer import anonymize_text
from miner import analyze_entities

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
    analysis = analyze_entities(entities)

    print("\n=== Найденные сущности ===")
    for entity in entities:
        print(entity)

    print("\n=== Data Mining анализ ===")
    print("Количество сущностей:", analysis["entity_counts"])
    print("Риск-паттерны:", analysis["patterns"])
    print("Risk score:", analysis["risk_score"])
    print("Risk level:", analysis["risk_level"])
    print("Всего сущностей:", analysis["total_entities"])

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
    risk_scores = []
    risk_levels = []
    total_entities_list = []
    entity_count_summaries = []

    for text in df["text"]:
        text = str(text)

        entities = detect_all(text)
        analysis = analyze_entities(entities)
        anonymized_text, _ = anonymize_text(text, entities)

        anonymized_texts.append(anonymized_text)
        risk_scores.append(analysis["risk_score"])
        risk_levels.append(analysis["risk_level"])
        total_entities_list.append(analysis["total_entities"])
        entity_count_summaries.append(str(analysis["entity_counts"]))

    df["anonymized_text"] = anonymized_texts
    df["risk_score"] = risk_scores
    df["risk_level"] = risk_levels
    df["total_entities"] = total_entities_list
    df["entity_counts"] = entity_count_summaries

    saved_csv_path = save_dataframe_csv(df)

    print("\n=== CSV обработан ===")
    print(df)
    print(f"\nФайл сохранён: {saved_csv_path}")

    dataset_summary = build_dataset_summary(df)

    print("\n=== Data Mining сводка по CSV ===")
    print("Всего записей:", dataset_summary["total_records"])
    print("LOW risk:", dataset_summary["low_risk"])
    print("MEDIUM risk:", dataset_summary["medium_risk"])
    print("HIGH risk:", dataset_summary["high_risk"])
    print("Средний risk score:", dataset_summary["average_risk_score"])


def build_dataset_summary(df):
    total_records = len(df)
    low_risk = (df["risk_level"] == "LOW").sum()
    medium_risk = (df["risk_level"] == "MEDIUM").sum()
    high_risk = (df["risk_level"] == "HIGH").sum()
    average_risk_score = round(df["risk_score"].mean(), 2)

    return {
        "total_records": total_records,
        "low_risk": int(low_risk),
        "medium_risk": int(medium_risk),
        "high_risk": int(high_risk),
        "average_risk_score": average_risk_score,
    }


def main():
    try:
        process_txt()
        process_csv()

    except Exception as e:
        print("Ошибка:", e)


if __name__ == "__main__":
    main()