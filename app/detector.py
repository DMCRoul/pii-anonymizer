import re
import spacy


nlp = spacy.load("en_core_web_sm")

EMAIL_REGEX = r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}"
PHONE_REGEX = r"(\+?\d[\d\-\s]{7,}\d)"

IGNORED_PERSON_VALUES = {"Email", "Phone", "Telephone", "Телефон", "Имя", "Name"}


def detect_email_entities(text):
    entities = []

    for match in re.finditer(EMAIL_REGEX, text):
        entities.append({
            "type": "EMAIL",
            "value": match.group(),
            "start": match.start(),
            "end": match.end()
        })

    return entities


def detect_phone_entities(text):
    entities = []

    for match in re.finditer(PHONE_REGEX, text):
        entities.append({
            "type": "PHONE",
            "value": match.group(),
            "start": match.start(),
            "end": match.end()
        })

    return entities


def detect_named_entities(text):
    entities = []
    doc = nlp(text)

    for ent in doc.ents:
        value = ent.text.strip()

        if ent.label_ == "PERSON":
            if value not in IGNORED_PERSON_VALUES and len(value) > 2:
                entities.append({
                    "type": "PERSON",
                    "value": value,
                    "start": ent.start_char,
                    "end": ent.end_char
                })

        elif ent.label_ in ["GPE", "LOC"]:
            if len(value) > 1:
                entities.append({
                    "type": "LOCATION",
                    "value": value,
                    "start": ent.start_char,
                    "end": ent.end_char
                })

    return entities


def remove_duplicates(entities):
    unique_entities = []
    seen = set()

    for entity in entities:
        key = (entity["type"], entity["value"], entity["start"], entity["end"])
        if key not in seen:
            seen.add(key)
            unique_entities.append(entity)

    return unique_entities


def detect_all(text):
    email_entities = detect_email_entities(text)
    phone_entities = detect_phone_entities(text)
    ner_entities = detect_named_entities(text)

    all_entities = email_entities + phone_entities + ner_entities
    all_entities = remove_duplicates(all_entities)

    all_entities.sort(key=lambda x: x["start"])

    return all_entities