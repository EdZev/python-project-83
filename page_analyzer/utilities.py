from urllib.parse import urlparse
from validators.url import url


def is_valid_url(url_to_valid):
    return len(url_to_valid) <= 255 and url(url_to_valid)


def normalize_url(url_to_normalize):
    parsed_url = urlparse(url_to_normalize)
    return f'{parsed_url.scheme}://{parsed_url.netloc}'
