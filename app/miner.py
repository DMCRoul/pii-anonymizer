from collections import Counter


def count_entity_types(entities):
    counts = Counter()

    for entity in entities:
        counts[entity["type"]] += 1

    return dict(counts)


def detect_risk_patterns(entity_counts):
    patterns = []

    has_person = entity_counts.get("PERSON", 0) > 0
    has_email = entity_counts.get("EMAIL", 0) > 0
    has_phone = entity_counts.get("PHONE", 0) > 0
    has_location = entity_counts.get("LOCATION", 0) > 0

    if has_person and has_email:
        patterns.append("PERSON+EMAIL")

    if has_person and has_phone:
        patterns.append("PERSON+PHONE")

    if has_email and has_phone:
        patterns.append("EMAIL+PHONE")

    if has_person and has_email and has_phone:
        patterns.append("PERSON+EMAIL+PHONE")

    if has_person and has_location:
        patterns.append("PERSON+LOCATION")

    return patterns


def calculate_risk_score(entity_counts, patterns):
    score = 0

    score += entity_counts.get("PERSON", 0) * 2
    score += entity_counts.get("EMAIL", 0) * 3
    score += entity_counts.get("PHONE", 0) * 3
    score += entity_counts.get("LOCATION", 0) * 1

    if "PERSON+EMAIL" in patterns:
        score += 3

    if "PERSON+PHONE" in patterns:
        score += 3

    if "EMAIL+PHONE" in patterns:
        score += 2

    if "PERSON+EMAIL+PHONE" in patterns:
        score += 5

    return score


def classify_risk(score):
    if score >= 12:
        return "HIGH"
    elif score >= 6:
        return "MEDIUM"
    return "LOW"


def analyze_entities(entities):
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
    entity_counts = count_entity_types(entities)
    patterns = detect_risk_patterns(entity_counts)
    risk_score = calculate_risk_score(entity_counts, patterns)
    risk_level = classify_risk(risk_score)

    return {
        "entity_counts": entity_counts,
        "patterns": patterns,
        "risk_score": risk_score,
        "risk_level": risk_level,
        "total_entities": len(entities),
    }