# Yanfei Xiao (xiaofx)

import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from collections import deque
import sys
import time


ALLOWED_DOMAINS = {"eecs.umich.edu", "eecs.engin.umich.edu", "ece.engin.umich.edu", "cse.engin.umich.edu"}

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

def is_valid_url(url):
    parsed_url = urlparse(url)
    return parsed_url.netloc in ALLOWED_DOMAINS and parsed_url.scheme in {"http", "https"}


def crawl(seed_link, max_urls):
    start_time = time.time()  

    with open(seed_link, "r") as f:
        start_url = f.readline().strip()

    visited = {} # dict: {"domain": set{link1, link2, ...}}
    queue = deque([start_url]) # now place it in BFS queue 
    url_list = [] # for discovered URLs
    link_list = [] # for all the link connections between webpages




    # main BFS Loop for web crawling
    while queue and len(url_list) < max_urls: 
        url = queue.popleft()

        if url in visited:
            continue
        visited.add(url)
        url_list.append(url)

        try:
           
            response = requests.get(url, headers=HEADERS, timeout=5)
            print(f"Fetched {url} with status code {response.status_code}")

            # if response.status_code == 429:
            #     retry_after = int(response.headers.get("Retry-After", 5))  
            #     print(f"Rate limited! Waiting {retry_after} seconds...")
            #     time.sleep(retry_after)
            #     queue.append(url)  # try again later!
            #     continue  

            if response.status_code == 429:
                print(f"Skipping {url} due to persistent 429 errors.")
                continue
        
            if "text/html" not in response.headers["Content-Type"]:
                continue
            
            soup = BeautifulSoup(response.text, "html.parser")
            for link in soup.find_all("a", href=True):
                full_url = urljoin(url, link["href"])

                if is_valid_url(full_url) and full_url not in visited:
                    queue.append(full_url)
                    link_list.append((url, full_url))
        
        except requests.exceptions.RequestException:
            print(f"Failed to fetch {url}, skipping...")
            continue  

    end_time = time.time()
    elapsed_time = end_time - start_time  # Calculate elapsed time

  


    # Save outputs
    with open("crawler.output", "w") as f:
        f.write("\n".join(url_list))

    with open("links.output", "w") as f:
        for source, dest in link_list:
            f.write(f"({source}, {dest})\n")

    print(f"\nCrawler finished in {elapsed_time:.2f} seconds.")



if __name__ == "__main__":
    seed_link = sys.argv[1]  # starting seed link
    max_urls = int(sys.argv[2])  # max urls to find before stopping, such as 2500
    crawl(seed_link, max_urls)
