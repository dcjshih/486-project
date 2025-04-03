from urllib.parse import urljoin, urlparse, urlunparse
import urllib.robotparser
from crawler import ALLOWED_DOMAINS, ROBOTS_CACHE, HEADERS

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

def get_robots_parser(domain):
    """Fetch and parse robots.txt for a given domain, caching the results."""
    if domain in ROBOTS_CACHE:
        return ROBOTS_CACHE[domain]

    robots_url = f"https://{domain}/robots.txt"
    rp = urllib.robotparser.RobotFileParser()

    try:
        rp.set_url(robots_url)
        rp.read()
        ROBOTS_CACHE[domain] = rp
    except Exception as e:
        print(f"Failed to fetch robots.txt from {robots_url}: {e}")
        rp = None  # Assume no restrictions if fetching fails

    return rp

def is_allowed_by_robots(url):
    """Check if the URL is allowed by robots.txt."""
    domain = urlparse(url).netloc
    rp = get_robots_parser(domain)

    if rp and not rp.can_fetch(HEADERS["User-Agent"], url):
        print(f"Blocked by robots.txt: {url}")
        return False
    return True