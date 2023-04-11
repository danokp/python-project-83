from bs4 import BeautifulSoup
from validators.url import url as is_valid_url
from urllib.parse import urlsplit, urlunsplit


def normalize_url(url):
    scheme, netloc = (
        urlsplit(url).scheme.lower(),
        urlsplit(url).netloc.lower(),
    )
    if netloc.startswith('www.'):
        netloc = netloc[4:]
    return urlunsplit((scheme, netloc, '', '', ''))


def check_url(url):
    MAX_URL_LEN = 255

    errors = []
    normalized_url = normalize_url(url)
    if len(normalized_url) > MAX_URL_LEN or not is_valid_url(normalized_url):
        errors.append('Некорректный URL')
        if not url:
            errors.append('URL обязателен')
    return normalized_url, errors


def scrap_web_page(page):
    soup = BeautifulSoup(page.content, "html.parser")
    h1 = soup.h1
    title = soup.title
    content = soup.find('meta', attrs={'name': 'description'})
    return (
        truncate_string(h1.get_text(strip=True)) if h1 else '',
        truncate_string(title.get_text(strip=True)) if title else '',
        truncate_string(content['content']) if content else '',
    )


def truncate_string(string, limit=255, ending='...'):
    if len(string) <= 255:
        return string
    return string[:limit - len(ending)] + ending
