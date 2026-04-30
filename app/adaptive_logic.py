from detector import detect_base, detect_transformer_layer, merge_entities
from miner import analyze_entities


RISK_MODE_CONFIG = {
    "LOW": {
        "transformer_min_score": 0.80,
        "second_pass": False,
        "mode": "conservative",
    },
    "MEDIUM": {
        "transformer_min_score": 0.60,
        "second_pass": False,
        "mode": "standard",
    },
    "HIGH": {
        "transformer_min_score": 0.45,
        "second_pass": True,
        "mode": "aggressive",
    },
}


def run_adaptive_detection(text: str) -> dict:
    # 1) Базовая детекция всегда
    base_entities = detect_base(text)
    base_analysis = analyze_entities(base_entities)

    # 2) Data Mining выбирает режим
    risk_level = base_analysis["risk_level"]
    config = RISK_MODE_CONFIG[risk_level]

    # 3) Transformer подключается с нужным порогом
    transformer_entities = detect_transformer_layer(
        text,
        min_score=config["transformer_min_score"],
    )

    entities = merge_entities(base_entities, transformer_entities)
    final_analysis = analyze_entities(entities)

    # 4) При высоком риске делаем дополнительный проход
    if config["second_pass"]:
        second_pass_entities = detect_transformer_layer(
            text,
            min_score=0.35,
        )
        entities = merge_entities(entities, second_pass_entities)
        final_analysis = analyze_entities(entities)

    return {
        "entities": entities,
        "analysis": final_analysis,
        "base_analysis": base_analysis,
        "adaptive_mode": config["mode"],
        "transformer_min_score": config["transformer_min_score"],
        "second_pass": config["second_pass"],
    }