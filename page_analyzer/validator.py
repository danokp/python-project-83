from urllib.parse import urlsplit, urlunsplit


def normalize_url(url):
    scheme, netloc = (
        urlsplit(url).scheme.lower(),
        urlsplit(url).netloc.lower(),
    )
    if netloc.startswith('www.'):
        netloc = netloc[4:]
    return urlunsplit((scheme, netloc, '', '', ''))



