import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from collections import deque
import sys
import time
import json
from urllib.robotparser import RobotFileParser

# Allowed domains
ALLOWED_DOMAINS = set()

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

def is_valid_url(url):
    """Check if the URL is valid and belongs to the allowed domains."""
    parsed_url = urlparse(url)
    return parsed_url.netloc in ALLOWED_DOMAINS and parsed_url.scheme in {"http", "https"}

def extract_main_content(soup):
    # Remove scripts, styles, and unwanted elements
    for tag in soup(["script", "style", "header", "footer", "nav", "aside"]):
        tag.extract()

    # Extract text and normalize spacing
    text = soup.get_text(separator=" ").strip()
    text = " ".join(text.split())  # Remove excessive spaces

    return text

'''
    input:
        - seed_filename: .txt doc of 20 seed urls (both bad and good)
        - pos_keyword_filename: .txt doc of positive keywords
        - neg_keyword_filename: .txt doc of negative keywords
        - max_urls: maximum # of pages per domain 
    output: 
        - pos_output # {"link1": [keyword1, keyword2, keyword3, … keyword40], "link2": [keyword1, "", "", … ""] ...}
        - neg_output # {"link1": [keyword1, keyword2, keyword3, … keyword40], "link2": [keyword1, "", "", … ""] ...}
'''


def crawl(seed_filename, pos_keyword_filename, neg_keyword_filename, max_urls):
    
    pos_keyword_list = []
    neg_keyword_list = []
    seed_urls = []

    visited = {} # domain: set(url1, url2) this helps keep track of # of subpages < 100
    queue = deque(seed_urls)
    
    pos_output = {} 
    neg_output = {} 

    # read in files 
    with open(seed_filename, "r") as f:
        for line in f:
            seed_url = line.strip()
            seed_urls.append(seed_urls)
            # create ALLOWED_DOMAINS list based on seed url domains
            ALLOWED_DOMAINS.add(urlparse(seed_url).netloc)

    with open(pos_keyword_filename, "r") as f:
        for line in f:
            pos_keyword_list.append(line.strip())

    with open(neg_keyword_filename, "r") as f:
        for line in f:
            neg_keyword_list.append(line.strip())
    
    while queue: 
        url = queue.popleft()
        url_domain = urlparse(url).netloc

        if url in visited: 
            continue
        
        if not visited[url_domain]:
            visited[url_domain] = set(url)
        else:
            visited[url_domain].add(url)

        try:
            response = requests.get(url, headers=HEADERS, timeout=5)

            if response.status_code == 429:
                print(f"Skipping {url} due to persistent 429 errors.")
                continue

            if "text/html" not in response.headers["Content-Type"]:
                continue

            soup = BeautifulSoup(response.text, "html.parser")
            content = extract_main_content(soup)
            print(f"Webpage Content:\n {content}")

        except requests.exceptions.RequestException:
            print(f"Failed to fetch {url}, skipping...")
            continue 

        








    # # Main BFS loop for web crawling
    # while queue:
    #     url = queue.popleft()

    #     # if url is from domain that's maxed out
    #     if url in visited:
    #         continue
    #     visited.add(url)

    #     try:
    #         response = requests.get(url, headers=HEADERS, timeout=5)
    #         print(f"Fetched {url} with status code {response.status_code}")

    #         if response.status_code == 429:
    #             print(f"Skipping {url} due to persistent 429 errors.")
    #             continue

    #         if "text/html" not in response.headers["Content-Type"]:
    #             continue

    #         page_content = response.text
    #         keywords_found = check_keywords_in_page(page_content, keyword_list)

    #         # normalize text, check for abbreviations
    #         # check for keywords

    # #         # Add the URL and the keywords found to the output dictionary
    # #         output[url] = keywords_found

    #         # Parse the page for links
    #         soup = BeautifulSoup(page_content, "html.parser")
    #         for link in soup.find_all("a", href=True):
    #             full_url = urljoin(url, link["href"])

    #             if is_valid_url(full_url) and full_url not in visited:
    #                 queue.append(full_url)
    #                 link_list.append((url, full_url))

    #     except requests.exceptions.RequestException:
    #         print(f"Failed to fetch {url}, skipping...")
    #         continue

    # end_time = time.time()
    # elapsed_time = end_time - start_time  # Calculate elapsed time

    # # Save the dictionary output to a file
    # with open("positive_output.json", "w") as f:
    #     json.dump(pos_output, f, indent=4)
    # with open("negative_output.json", "w") as f:
    #     json.dump(pos_output, f, indent=4)

    # print(f"\nCrawler finished in {elapsed_time:.2f} seconds.")

if __name__ == "__main__":
    # Check command-line arguments
    if len(sys.argv) != 5:
        print("Usage: python crawler.py <seedURLs.txt> <pos_keywords.txt> <neg_keywords.txt> <max_urls>")
        sys.exit(1)

    seed_filename = sys.argv[1]
    positive_keyword_filename = sys.argv[2]
    negative_keyword_filename = sys.argv[3]
    max_urls = int(sys.argv[4])

    crawl(seed_filename, positive_keyword_filename, negative_keyword_filename, max_urls)
