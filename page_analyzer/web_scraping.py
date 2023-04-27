from bs4 import BeautifulSoup


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
