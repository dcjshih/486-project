import ahocorasick
from fuzzywuzzy import fuzz

def build_aho_corasick(keywords):
    A = ahocorasick.Automaton()
    for keyword in keywords:
        A.add_word(keyword.lower(), keyword)
    A.make_automaton()
    return A

def check_keywords(text, automaton, keywords, fuzzy_threshold=80):
    exact_matches = set()
    for _, found_keyword in automaton.iter(text.lower()):
        exact_matches.add(found_keyword)

    fuzzy_matches = set()
    for keyword in keywords:
        match_score = fuzz.partial_ratio(keyword.lower(), text.lower())
        if match_score >= fuzzy_threshold:
            fuzzy_matches.add(keyword)

    return exact_matches, fuzzy_matches