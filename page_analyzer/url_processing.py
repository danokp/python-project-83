from validators.url import url as is_valid_url
from urllib.parse import urlsplit, urlunsplit


def normalize_url(url):
    scheme, netloc = (
        urlsplit(url).scheme.lower(),
        urlsplit(url).netloc.lower(),
    )
    return urlunsplit((scheme, netloc, '', '', ''))


def check_url(url):
    MAX_URL_LEN = 255

    errors = []
    normalized_url = normalize_url(url)
    if not url:
        errors.extend((
            'Некорректный URL',
            'URL обязателен'
        ))
    elif len(normalized_url) > MAX_URL_LEN or not is_valid_url(normalized_url):
        errors.append('Некорректный URL')
    return normalized_url, errors
