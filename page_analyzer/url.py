from urllib.parse import urlparse
import validators


def normalize_url(url_string):
    parsed = urlparse(url_string)
    return f"{parsed.scheme}://{parsed.netloc}".lower()


def validate_url(url_string):
    if not url_string or len(url_string) > 255 or not validators.url(url_string):
        return ['Некорректный URL']
    return []