from urllib.parse import urljoin, urlparse
from crawler import ALLOWED_DOMAINS

def find_domain(url):
    parsed = urlparse(url)
    return parsed.netloc

def extension_filtering(url):
    allowed_extensions = ['.html', '.htm']
    parsed_url = urlparse(url)
    path = parsed_url.path
    
    if '.' not in path:
        return True

    file_extension = path.split('.')[-1] if '.' in path else ''
    if file_extension.lower() in [ext.lstrip('.') for ext in allowed_extensions]:
        return True
    return False


def is_valid_url(url):
    parsed_url = urlparse(url)
    return parsed_url.netloc in ALLOWED_DOMAINS and parsed_url.scheme in {"http", "https"}