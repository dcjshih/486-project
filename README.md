# Eco-Search

### Overview
This project implements a search engine fine-tuned for clothing products for shopping.
Here are the main parts:
1. `seedURLs.txt`: initial file to start the crawling of keywords and product pages
2. `crawler.py`: implements a crawler. The web crawler starts from a set of seed URLs and recursively explores links while performing keyword matching. It extracts text content from web pages and checks for the presence of predefined positive and negative keywords. The results are stored in output files. These files are `websites_data.csv` for the websites to train on, as well as `pos_keywords.txt` and `neg_keywords.txt` for the keywords to use in the fine-tuning of the model.
3. `Project.ipynb`: This contains the implementation of the model fine-tuned with the data from `crawler.py`
4. `Retrieval1.py`: This is the backend of the search engine. It contains POST requests to interact with the user.
5. `Retrieval_tests.py`: This is the file that was used to test the search engine.
6. `templates/index.html` and `static/app.js`: These contain the front-end of the search engine
7. `index_old.html`: This is a deprecated version of the front-end. This version is a bit more sophisticated, but ran us into problems to connect with the front-end, so we constructed a more simple version. A next step could be to re-implement this front-end to the back-end.
8. `websites_data.csv`: Raw dataset 
9. `website_embeddings.pt`: This file contains the embeddings related to each website. It can be used to calculate cosine similarity with the query embedding.
10. `fine_tune_model.ipynb`: This file contains the code for preprocessing, creating the dataset for fine-tuning, and fine-tuning the MiniLM model.

## Crawler
# Features
- Extracts and follows links within the same domain as the seed URLs.
- Filters out non-HTML content.
- Checks robots.txt compliance before crawling.
- Matches exact and fuzzy positive and negative keywords.
- Limits the number of pages crawled per domain.
- Saves results in structured output files.

# Requirements
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

# Usage
Run the crawler using the following command:
```sh
python crawler.py <seedURLs> <pos_keywords> <neg_keywords> <max_urls>
```
Where:
- `<seedURLs>`: Path to a file containing seed URLs (one per line).
- `<pos_keywords>`: Path to a file containing positive keywords.
- `<neg_keywords>`: Path to a file containing negative keywords.
- `<max_urls>`: Maximum number of pages to crawl per domain.

# Example
```sh
python crawler.py seeds.txt positive_keywords.txt negative_keywords.txt 10
```

# Output
The crawler generates two output files:
- `output_pos.txt`: Contains URLs and detected positive keywords.
- `output_neg.txt`: Contains URLs and detected negative keywords.

## Model Implementation:
- MiniLM is a compact and efficient variation of BERT model.
- MiniLM model was fine-tuned on a small dataset using cosine similarity loss and trained on 1 epoch to avoid overfitting.
- The fine-tuned model is used to encode every website's extracted text to create word embeddings

## Retrieval:
# Features

- **Search Functionality:** Users can input queries related to sustainable fashion, and the engine will return the top relevant websites based on the provided query.
- **Fine-Tuned Model:** The engine utilizes a pre-trained SentenceTransformer model fine-tuned on a specific dataset of sustainable fashion-related keywords.
- **API:** The engine provides a REST API that accepts user queries and returns the most relevant websites.

# Methods Used

- **Flask:** A micro web framework used for building the backend of the application.
- **Sentence-Transformers:** A library to encode text data into embeddings, which are then used for computing similarities.
- **PyTorch:** A deep learning framework used for tensor operations and model inference.
- **Flask-CORS:** A Flask extension to handle Cross-Origin Resource Sharing (CORS).
- **HTML/CSS:** For frontend rendering (using `index.html`).

# Requirements

To run the project, you will need to have the following Python packages installed:

- Flask
- Flask-CORS
- Sentence-Transformers
- PyTorch

You can install the required dependencies by running:

```bash
pip install -r requirements.txt
```

## Usage
```bash
python3 Retrieval1.py
```

This will open the browswer and show the front-end of the model.
From here it is possible to test by inputting sample searches on the search bar.

## Testing
To run tests: 
```bash
python3 Retrieval_tests.py
```

