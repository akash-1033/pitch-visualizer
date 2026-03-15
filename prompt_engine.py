import re

STYLE_SUFFIX = (
    "cinematic composition, dramatic lighting, highly detailed, "
    "photorealistic, 8k, sharp focus, professional photography"
)

SETTING_HINTS = {
    "night": "moonlit, deep shadows, ambient glow",
    "day": "golden hour sunlight, long shadows, warm tones",
    "city": "urban skyline, neon reflections, steel and glass",
    "forest": "dense canopy, dappled light, mist between trees",
    "ocean": "crashing waves, salt spray, vast horizon",
    "interior": "warm interior lighting, textured walls, depth of field",
    "storm": "dark storm clouds, lightning on the horizon, turbulent sky",
    "desert": "scorched earth, heat shimmer, endless dunes",
}

ACTION_HINTS = {
    "run": "motion blur, dynamic angle, urgency",
    "walk": "steady movement, environmental storytelling",
    "look": "expressive face, shallow depth of field, emotional close-up",
    "fight": "kinetic energy, dramatic pose, high-contrast lighting",
    "speak": "expressive gesture, warm portrait lighting",
    "sit": "quiet contemplation, environmental context, soft light",
    "stand": "commanding presence, strong vertical composition",
    "fall": "vertiginous angle, motion, atmospheric depth",
}


def _detect_context_hints(sentence: str) -> list[str]:
    lower = sentence.lower()
    hints = []
    for keyword, descriptor in SETTING_HINTS.items():
        if keyword in lower:
            hints.append(descriptor)
    for keyword, descriptor in ACTION_HINTS.items():
        pattern = rf"\b{keyword}(s|ed|ing)?\b"
        if re.search(pattern, lower):
            hints.append(descriptor)
    return hints


def _extract_subjects(sentence: str) -> str:
    # Naive subject extraction: take the first noun phrase worth of words
    # before the first verb indicator. Good enough for prompt enrichment.
    words = sentence.split()
    subjects = []
    stop_words = {"is", "are", "was", "were", "has", "have", "had", "be", "been"}
    for word in words[:6]:
        if word.lower() in stop_words:
            break
        subjects.append(word)
    return " ".join(subjects) if subjects else ""


def build_prompt(scene_text: str) -> str:
    hints = _detect_context_hints(scene_text)
    subject_fragment = _extract_subjects(scene_text)

    parts = [scene_text.rstrip(".")]

    if hints:
        parts.append(", ".join(hints))

    if subject_fragment:
        parts.append(f"featuring {subject_fragment}")

    parts.append(STYLE_SUFFIX)

    return ", ".join(parts)
