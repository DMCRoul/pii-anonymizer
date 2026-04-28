import argparse
from pathlib import Path

from loader import load_text_file, load_csv_file
from anonymizer import anonymize_text
from writer import (
    save_anonymized_text,
    save_replacements_csv,
    save_dataframe_csv,
    save_summary,
)
from adaptive_logic import run_adaptive_detection


def process_txt(file_path: str) -> None:
    text = load_text_file(file_path)

    print("=== Исходный TXT ===\n")
    print(text)

    result = run_adaptive_detection(text)
    entities = result["entities"]
    analysis = result["analysis"]

    print("\n=== Adaptive detection ===")
    print("Base risk level:", result["base_analysis"]["risk_level"])
    print("Adaptive mode:", result["adaptive_mode"])
    print("Transformer threshold:", result["transformer_min_score"])
    print("Second pass:", result["second_pass"])

    print("\n=== Найденные сущности ===")
    for entity in entities:
        print(entity)

    print("\n=== Data Mining анализ ===")
    print("Количество сущностей:", analysis["entity_counts"])
    print("Риск-паттерны:", analysis["patterns"])
    print("Risk score:", analysis["risk_score"])
    print("Risk level:", analysis["risk_level"])
    print("Причины риска:")
    for reason in analysis["risk_reasons"]:
        print("-", reason)
    print("Всего сущностей:", analysis["total_entities"])

    anonymized_text, replacements = anonymize_text(text, entities)

    print("\n=== Анонимизированный TXT ===\n")
    print(anonymized_text)

    save_anonymized_text(anonymized_text)
    save_replacements_csv(replacements)

    print("\nTXT обработан и сохранён в output/")


def build_dataset_summary(df) -> dict:
    total_records = len(df)
    low_risk = (df["risk_level"] == "LOW").sum()
    medium_risk = (df["risk_level"] == "MEDIUM").sum()
    high_risk = (df["risk_level"] == "HIGH").sum()
    average_risk_score = round(df["risk_score"].mean(), 2)

    records_with_pii = int((df["total_entities"] > 0).sum())
    high_risk_percentage = round((high_risk / total_records) * 100, 2) if total_records else 0

    entity_totals = {"PERSON": 0, "EMAIL": 0, "PHONE": 0, "LOCATION": 0}
    pattern_totals = {}

    for _, row in df.iterrows():
        entity_counts_str = str(row["entity_counts"])

        for entity_type in entity_totals:
            if entity_type in entity_counts_str:
                try:
                    import ast
                    parsed_counts = ast.literal_eval(entity_counts_str)
                    for key, value in parsed_counts.items():
                        if key in entity_totals:
                            entity_totals[key] += value
                except Exception:
                    pass
                break

    most_common_entity_type = None
    if any(entity_totals.values()):
        most_common_entity_type = max(entity_totals, key=entity_totals.get)

    return {
        "total_records": int(total_records),
        "records_with_pii": records_with_pii,
        "low_risk": int(low_risk),
        "medium_risk": int(medium_risk),
        "high_risk": int(high_risk),
        "high_risk_percentage": high_risk_percentage,
        "average_risk_score": average_risk_score,
        "most_common_entity_type": most_common_entity_type,
        "entity_totals": entity_totals,
    }


def process_csv(file_path: str) -> None:
    df = load_csv_file(file_path)

    if "text" not in df.columns:
        raise ValueError("В CSV нет колонки 'text'")

    anonymized_texts = []
    risk_scores = []
    risk_levels = []
    total_entities_list = []
    entity_count_summaries = []
    adaptive_modes = []
    thresholds = []
    second_pass_flags = []
    risk_reasons_list = []

    for text in df["text"]:
        text = str(text)

        result = run_adaptive_detection(text)
        entities = result["entities"]
        analysis = result["analysis"]

        anonymized_text, _ = anonymize_text(text, entities)

        anonymized_texts.append(anonymized_text)
        risk_scores.append(analysis["risk_score"])
        risk_levels.append(analysis["risk_level"])
        total_entities_list.append(analysis["total_entities"])
        entity_count_summaries.append(str(analysis["entity_counts"]))
        adaptive_modes.append(result["adaptive_mode"])
        thresholds.append(result["transformer_min_score"])
        second_pass_flags.append(result["second_pass"])
        risk_reasons_list.append(" | ".join(analysis["risk_reasons"]))

    df["anonymized_text"] = anonymized_texts
    df["risk_score"] = risk_scores
    df["risk_level"] = risk_levels
    df["total_entities"] = total_entities_list
    df["entity_counts"] = entity_count_summaries
    df["adaptive_mode"] = adaptive_modes
    df["transformer_threshold"] = thresholds
    df["second_pass"] = second_pass_flags
    df["risk_reasons"] = risk_reasons_list

    saved_csv_path = save_dataframe_csv(df)

    print("\n=== CSV обработан ===")
    print(df)
    print(f"\nФайл сохранён: {saved_csv_path}")

    dataset_summary = build_dataset_summary(df)
    summary_path = save_summary(dataset_summary)

    print("\n=== Data Mining сводка по CSV ===")
    print("Всего записей:", dataset_summary["total_records"])
    print("LOW risk:", dataset_summary["low_risk"])
    print("MEDIUM risk:", dataset_summary["medium_risk"])
    print("HIGH risk:", dataset_summary["high_risk"])
    print("Средний risk score:", dataset_summary["average_risk_score"])
    print("Summary saved:", summary_path)

def main() -> None:
    parser = argparse.ArgumentParser(
        description="PII detection, anonymization and data mining tool"
    )
    parser.add_argument("--file", required=True, help="Path to input file (.txt or .csv)")
    args = parser.parse_args()

    file_path = args.file
    suffix = Path(file_path).suffix.lower()

    try:
        if suffix == ".txt":
            process_txt(file_path)
        elif suffix == ".csv":
            process_csv(file_path)
        else:
            raise ValueError("Поддерживаются только .txt и .csv файлы")
    except Exception as e:
        print("Ошибка:", e)


if __name__ == "__main__":
    main()