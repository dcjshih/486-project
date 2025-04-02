from urllib.parse import urljoin, urlparse, urlunparse
from crawler import ALLOWED_DOMAINS

def find_domain(url):
    parsed = urlparse(url)
    return parsed.netloc

def normalize_url(url):
    parsed_url = urlparse(url)
    # switch to https
    scheme = "https"
    # removing fragments + getting rid of trailing / 
    netloc = parsed_url.netloc
    path = parsed_url.path.rstrip("/") if parsed_url.path != "/" else "/"
    # reconstruct
    clean_url = urlunparse((scheme, netloc, path, parsed_url.params, parsed_url.query, ""))
    return clean_url

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