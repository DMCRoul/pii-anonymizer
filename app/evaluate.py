import pandas as pd

from adaptive_logic import run_adaptive_detection


def parse_expected_types(value: str) -> set:
    if pd.isna(value) or str(value).strip() == "":
        return set()

    return {
        item.strip()
        for item in str(value).split(",")
        if item.strip()
    }


def get_detected_types(text: str) -> set:
    result = run_adaptive_detection(text)
    entities = result["entities"]

    return {
        entity["type"]
        for entity in entities
    }


def calculate_metrics(tp: int, fp: int, fn: int) -> dict:
    precision = tp / (tp + fp) if (tp + fp) else 0
    recall = tp / (tp + fn) if (tp + fn) else 0
    f1 = (
        2 * precision * recall / (precision + recall)
        if (precision + recall)
        else 0
    )

    return {
        "precision": round(precision, 3),
        "recall": round(recall, 3),
        "f1_score": round(f1, 3),
    }


def evaluate(file_path: str = "data/evaluation.csv") -> None:
    df = pd.read_csv(file_path)

    total_tp = 0
    total_fp = 0
    total_fn = 0

    rows = []

    for _, row in df.iterrows():
        text = str(row["text"])
        expected = parse_expected_types(row["expected_types"])
        detected = get_detected_types(text)

        tp = len(expected & detected)
        fp = len(detected - expected)
        fn = len(expected - detected)

        total_tp += tp
        total_fp += fp
        total_fn += fn

        rows.append({
            "text": text,
            "expected": ",".join(sorted(expected)),
            "detected": ",".join(sorted(detected)),
            "tp": tp,
            "fp": fp,
            "fn": fn,
        })

    metrics = calculate_metrics(total_tp, total_fp, total_fn)

    result_df = pd.DataFrame(rows)
    result_df.to_csv("output/evaluation_results.csv", index=False)

    print("\n=== Evaluation results ===")
    print(result_df)

    print("\n=== Metrics ===")
    print("True positives:", total_tp)
    print("False positives:", total_fp)
    print("False negatives:", total_fn)
    print("Precision:", metrics["precision"])
    print("Recall:", metrics["recall"])
    print("F1-score:", metrics["f1_score"])

    print("\nResults saved to output/evaluation_results.csv")


if __name__ == "__main__":
    evaluate()