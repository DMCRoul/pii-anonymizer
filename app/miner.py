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