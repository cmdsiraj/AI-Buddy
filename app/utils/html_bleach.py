import bleach

ALLOWED_TAGS = ["b", "i", "em", "strong", "a", "img"]
ALLOWED_ATTRS = {
    "a": ["href", "target", "rel"],
    "img": ["src"],
}

def sanitize_html(content: str) -> str:
    return bleach.clean(content, tags=ALLOWED_TAGS, attributes=ALLOWED_ATTRS, strip=True)
