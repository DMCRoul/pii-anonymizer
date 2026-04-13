from transformers import pipeline

ner_pipeline = pipeline(
    "ner",
    model="dslim/bert-base-NER",
    aggregation_strategy="simple"
)


def detect_transformer_entities(text):
    results = ner_pipeline(text)

    entities = []

    for ent in results:
        label = ent["entity_group"]
        value = ent["word"].strip()
        start = ent["start"]
        end = ent["end"]

        if "##" in value:
            continue

        if len(value) < 2:
            continue

        if label == "PER":
            entities.append({
                "type": "PERSON",
                "value": value,
                "start": start,
                "end": end
            })

        elif label == "LOC":
            entities.append({
                "type": "LOCATION",
                "value": value,
                "start": start,
                "end": end
            })

    return entities