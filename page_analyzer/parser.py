from bs4 import BeautifulSoup


def truncate(text, limit=200):
    if text and len(text) > limit:
        return text[:limit] + '...'
    return text


def parse_html(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')

    h1_tag = soup.find('h1')
    h1 = h1_tag.get_text(strip=True) if h1_tag else None

    title_tag = soup.find('title')
    title = title_tag.get_text(strip=True) if title_tag else None

    description_tag = soup.find('meta', attrs={'name': 'description'})
    description = None
    if description_tag and description_tag.get('content'):
        description = description_tag['content'].strip()

    return {
        'h1': truncate(h1),
        'title': truncate(title),
        'description': truncate(description)
    }