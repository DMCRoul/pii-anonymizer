from collections import Counter


def analyze_entities(entities: list[dict]) -> dict:
    entity_types = [entity["type"] for entity in entities]
    entity_counts = dict(Counter(entity_types))
    total_entities = len(entities)

    risk_score = 0
    patterns = []
    risk_reasons = []

    has_person = entity_counts.get("PERSON", 0) > 0
    has_email = entity_counts.get("EMAIL", 0) > 0
    has_phone = entity_counts.get("PHONE", 0) > 0
    has_location = entity_counts.get("LOCATION", 0) > 0

    # базовые баллы
    risk_score += entity_counts.get("PERSON", 0) * 2
    risk_score += entity_counts.get("EMAIL", 0) * 3
    risk_score += entity_counts.get("PHONE", 0) * 3
    risk_score += entity_counts.get("LOCATION", 0) * 1

    # паттерны
    if has_person and has_email:
        patterns.append("PERSON+EMAIL")
        risk_score += 3
        risk_reasons.append("Person name combined with email address")

    if has_person and has_phone:
        patterns.append("PERSON+PHONE")
        risk_score += 3
        risk_reasons.append("Person name combined with phone number")

    if has_email and has_phone:
        patterns.append("EMAIL+PHONE")
        risk_score += 4
        risk_reasons.append("Multiple direct contact identifiers detected")

    if has_person and has_email and has_phone:
        patterns.append("PERSON+EMAIL+PHONE")
        risk_score += 5
        risk_reasons.append("Pattern PERSON+EMAIL+PHONE indicates possible PII leakage")

    if has_person and has_location:
        patterns.append("PERSON+LOCATION")
        risk_score += 2
        risk_reasons.append("Person name combined with location")

    if total_entities >= 4:
        risk_score += 2
        risk_reasons.append("High number of sensitive entities in one text")

    # определение уровня риска
    if risk_score >= 15:
        risk_level = "HIGH"
    elif risk_score >= 6:
        risk_level = "MEDIUM"
    else:
        risk_level = "LOW"

    if not risk_reasons:
        risk_reasons.append("No strong sensitive data patterns detected")

    return {
        "entity_counts": entity_counts,
        "patterns": patterns,
        "risk_score": risk_score,
        "risk_level": risk_level,
        "risk_reasons": risk_reasons,
        "total_entities": total_entities,
    }