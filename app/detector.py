import re

import spacy

from transformer_detector import detect_transformer_entities


nlp = spacy.load("en_core_web_sm")

EMAIL_REGEX = r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}"
PHONE_REGEX = r"(\+?\d[\d\-\s]{7,}\d)"

IGNORED_PERSON_VALUES = {
    "Email",
    "Phone",
    "Telephone",
    "Телефон",
    "Имя",
    "Name",
}


def detect_email_entities(text: str) -> list[dict]:
    entities = []

    for match in re.finditer(EMAIL_REGEX, text):
        entities.append(
            {
                "type": "EMAIL",
                "value": match.group(),
                "start": match.start(),
                "end": match.end(),
                "source": "regex",
            }
        )

    return entities


def detect_phone_entities(text: str) -> list[dict]:
    entities = []

    for match in re.finditer(PHONE_REGEX, text):
        entities.append(
            {
                "type": "PHONE",
                "value": match.group(),
                "start": match.start(),
                "end": match.end(),
                "source": "regex",
            }
        )

    return entities


def detect_named_entities(text: str) -> list[dict]:
    entities = []
    doc = nlp(text)

    for ent in doc.ents:
        value = ent.text.strip()

        if ent.label_ == "PERSON":
            if value not in IGNORED_PERSON_VALUES and len(value) > 2:
                entities.append(
                    {
                        "type": "PERSON",
                        "value": value,
                        "start": ent.start_char,
                        "end": ent.end_char,
                        "source": "spacy",
                    }
                )

        elif ent.label_ in ["GPE", "LOC"]:
            if len(value) > 1:
                entities.append(
                    {
                        "type": "LOCATION",
                        "value": value,
                        "start": ent.start_char,
                        "end": ent.end_char,
                        "source": "spacy",
                    }
                )

    fallback_pattern = r"\bin\s+([A-Z][a-z]+)"

    for match in re.finditer(fallback_pattern, text):
        city = match.group(1)
        entities.append(
            {
                "type": "LOCATION",
                "value": city,
                "start": match.start(1),
                "end": match.end(1),
                "source": "spacy_fallback",
            }
        )

    return entities


def remove_duplicates(entities: list[dict]) -> list[dict]:
    seen = set()
    unique_entities = []

    for entity in sorted(entities, key=lambda x: (x["start"], x["end"], x["type"])):
        key = (
            entity["type"],
            entity["start"],
            entity["end"],
            entity["value"],
        )

        if key not in seen:
            seen.add(key)
            unique_entities.append(entity)

    return unique_entities


def remove_overlaps(entities: list[dict]) -> list[dict]:
    if not entities:
        return []

    entities = sorted(
        entities,
        key=lambda x: (x["start"], -(x["end"] - x["start"])),
    )

    filtered = []

    for entity in entities:
        overlap = False

        for kept in filtered:
            if not (
                entity["end"] <= kept["start"]
                or entity["start"] >= kept["end"]
            ):
                overlap = True
                break

        if not overlap:
            filtered.append(entity)

    return filtered


def detect_base(text: str) -> list[dict]:
    entities = []

    entities.extend(detect_email_entities(text))
    entities.extend(detect_phone_entities(text))
    entities.extend(detect_named_entities(text))

    entities = remove_duplicates(entities)
    entities = remove_overlaps(entities)

    return entities


def detect_transformer_layer(text: str, min_score: float = 0.60) -> list[dict]:
    entities = detect_transformer_entities(text, min_score=min_score)

    entities = remove_duplicates(entities)
    entities = remove_overlaps(entities)

    return entities


def merge_entities(*entity_groups: list[dict]) -> list[dict]:
    merged = []

    for group in entity_groups:
        merged.extend(group)

    merged = remove_duplicates(merged)
    merged = remove_overlaps(merged)

    return merged


def detect_all(text: str, transformer_min_score: float = 0.60) -> list[dict]:
    base_entities = detect_base(text)
    transformer_entities = detect_transformer_layer(
        text,
        min_score=transformer_min_score,
    )

    return merge_entities(base_entities, transformer_entities)