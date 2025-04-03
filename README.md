# Keyword Matching Web Crawler for Eco-Search

## Overview
This project implements a web crawler that starts from a set of seed URLs and recursively explores links while performing keyword matching. It extracts text content from web pages and checks for the presence of predefined positive and negative keywords. The results are stored in output files.

## Features
- Extracts and follows links within the same domain as the seed URLs.
- Filters out non-HTML content.
- Checks robots.txt compliance before crawling.
- Matches exact and fuzzy positive and negative keywords.
- Limits the number of pages crawled per domain.
- Saves results in structured output files.

## Requirements
- **Python 3.x**
- Required Python libraries:
  - `requests`
  - `beautifulsoup4`
  - `urllib`
  - `collections`
  - `ahocorasick`
  - `fuzzywuzzy`

Install missing dependencies using:
```sh
pip install requests beautifulsoup4 ahocorasick fuzzywuzzy
```

## Usage
Run the crawler using the following command:
```sh
python crawler.py <seedURLs> <pos_keywords> <neg_keywords> <max_urls>
```
Where:
- `<seedURLs>`: Path to a file containing seed URLs (one per line).
- `<pos_keywords>`: Path to a file containing positive keywords.
- `<neg_keywords>`: Path to a file containing negative keywords.
- `<max_urls>`: Maximum number of pages to crawl per domain.

### Example
```sh
python crawler.py seeds.txt positive_keywords.txt negative_keywords.txt 10
```

## Output
The crawler generates two output files:
- `output_pos.txt`: Contains URLs and detected positive keywords.
- `output_neg.txt`: Contains URLs and detected negative keywords.

