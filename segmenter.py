import nltk

_downloaded = False


def _ensure_punkt():
    global _downloaded
    if _downloaded:
        return
    try:
        nltk.data.find("tokenizers/punkt_tab")
    except LookupError:
        nltk.download("punkt_tab", quiet=True)
    _downloaded = True


def segment_narrative(text: str) -> list[str]:
    _ensure_punkt()
    sentences = nltk.sent_tokenize(text.strip())
    return [s.strip() for s in sentences if s.strip()]
