from faker import Faker

fake = Faker()


def generate_fake_value(entity_type):
    if entity_type == "PERSON":
        return fake.name()

    elif entity_type == "EMAIL":
        return fake.email()

    elif entity_type == "PHONE":
        return fake.phone_number()

    elif entity_type == "LOCATION":
        return fake.city()

    return "[REDACTED]"


def anonymize_text(text, entities):
    anonymized_text = text

    # важно — идем с конца, чтобы индексы не ломались
    sorted_entities = sorted(entities, key=lambda x: x["start"], reverse=True)

    replacements = []

    for entity in sorted_entities:
        fake_value = generate_fake_value(entity["type"])

        start = entity["start"]
        end = entity["end"]

        anonymized_text = (
            anonymized_text[:start]
            + fake_value
            + anonymized_text[end:]
        )

        replacements.append({
            "original": entity["value"],
            "replacement": fake_value,
            "type": entity["type"]
        })

    return anonymized_text, replacements