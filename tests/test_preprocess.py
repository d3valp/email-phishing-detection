from src.preprocess import clean_text
def test_clean_text_replaces_urls():
    raw = "Click now: https://example.com/login !!!"
    cleaned = clean_text(raw)
    assert "url" in cleaned.lower()
    assert "https" not in cleaned.lower()
