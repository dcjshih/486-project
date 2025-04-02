from keyword_matching import *
from helper import *
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from collections import deque, defaultdict
import sys
import time
import pprint

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

def crawler(seed_list, pos_keyword_list, neg_keyword_list, max_suburls):
    start_time = time.time()
    visited = defaultdict(set)
    output_pos = defaultdict(lambda: [''] * 36)
    output_neg = defaultdict(lambda: [''] * 36)
    queue = deque(seed_list)
    max_url = max_suburls * len(seed_list)

    while queue and len(visited) < max_url:
        url = queue.popleft()
        url_domain = find_domain(url)
        if url_domain in visited and url in visited[url_domain]: 
            continue

        try:
            response = requests.get(url, headers=HEADERS, timeout=5)

            if response.status_code == 429:
                print(f"Skipping {url} due to persistent 429 errors.")
                continue
        
            if "text/html" not in response.headers["Content-Type"]:
                continue

            soup = BeautifulSoup(response.text, "html.parser")
            for tag in soup(["script", "style", "header", "footer", "nav", "aside"]):
                tag.decompose()
            
            text = soup.get_text(separator="\n", strip=True)

            ### extracting keywords ###
            automaton_neg = build_aho_corasick(neg_keyword_list)
            automaton_pos = build_aho_corasick(pos_keyword_list)

            exact_neg, fuzzy_neg = check_keywords(text, automaton_neg, neg_keyword_list)
            negative = exact_neg.union(fuzzy_neg)
            exact_pos, fuzzy_pos = check_keywords(text, automaton_pos, pos_keyword_list)
            positive = exact_pos.union(fuzzy_pos)

            output_neg[url] = list(negative)[:len(neg_keyword_list)] + [''] * (len(neg_keyword_list) - len(negative))
            output_pos[url] = list(positive)[:len(pos_keyword_list)] + [''] * (len(pos_keyword_list) - len(positive))


        except requests.exceptions.RequestException:
            print(f"Failed to fetch {url}, skipping...")
            continue  
        

def main():
    if len(sys.argv) != 5:
        print("Usage: python crawler.py <seedURLs> <pos_keywords> <neg_keywords> <max_urls>")
        sys.exit(1)

    seed_filename = sys.argv[1]
    seed_list = []
    positive_keyword_filename = sys.argv[2]
    pos_keyword_list = []
    negative_keyword_filename = sys.argv[3]
    neg_keyword_list = []
    max_suburls = int(sys.argv[4])

    with open(seed_filename, "r") as f:
        for line in f:
            seed_url = line.strip()
            seed_list.append(seed_url)
            # create ALLOWED_DOMAINS list based on seed url domains
            ALLOWED_DOMAINS.append(urlparse(seed_url).netloc)

    with open(positive_keyword_filename, "r") as f:
        for line in f:
            pos_keyword_list.append(line.strip())

    with open(negative_keyword_filename, "r") as f:
        for line in f:
            neg_keyword_list.append(line.strip())
    
    crawler(seed_list, pos_keyword_list, neg_keyword_list, max_suburls)

if __name__ == "__main__":
    main()