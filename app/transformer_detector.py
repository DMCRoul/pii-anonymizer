from transformers import pipeline

ner_pipeline = pipeline(
    "ner",
    model="dslim/bert-base-NER",
    aggregation_strategy="simple",
)

LABEL_MAP = {
    "PER": "PERSON",
    "LOC": "LOCATION",
}

def detect_transformer_entities(text: str, min_score: float = 0.60) -> list[dict]:
    results = ner_pipeline(text)
    entities: list[dict] = []

    for ent in results:
        label = ent.get("entity_group")
        value = ent.get("word", "").strip()
        score = float(ent.get("score", 0.0))
        start = ent.get("start")
        end = ent.get("end")

        if label not in LABEL_MAP:
            continue
        if score < min_score:
            continue
        if "##" in value:
            continue
        if len(value) < 2:
            continue
        if start is None or end is None:
            continue

        entities.append(
            {
                "type": LABEL_MAP[label],
                "value": value,
                "start": start,
                "end": end,
                "score": round(score, 4),
                "source": "transformer",
            }
        )

    return entities