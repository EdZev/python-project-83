from urllib.parse import urlparse
from validators.url import url
from bs4 import BeautifulSoup


def is_valid_url(url_to_valid):
    return len(url_to_valid) <= 255 and url(url_to_valid)


def normalize_url(url_to_normalize):
    parsed_url = urlparse(url_to_normalize)
    return f'{parsed_url.scheme}://{parsed_url.netloc}'


def get_seo_data(content):
    seo_data = {}
    soup = BeautifulSoup(content, 'html.parser')

    h1 = soup.h1
    seo_data['h1'] = h1.string if h1 else '-'

    title = soup.title.string
    seo_data['title'] = title.string if title else '-'

    description = soup.find('meta', attrs={'name': 'description'})
    seo_data['description'] = description.get('content') \
        if description else '-'

    return seo_data
