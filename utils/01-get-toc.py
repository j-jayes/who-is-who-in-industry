"""
This script fetches the Table of Contents (TOC) from a series of online biographical books and extracts the starting page numbers for each letter of the Swedish alphabet. The TOCs are then saved as YAML files in the "data/book_info" directory.

The script is specifically designed to handle the following book codes and their corresponding URLs:
- vemindu: http://runeberg.org/vemindu/

The script requires the following Python libraries to be installed:
- requests
- beautifulsoup4
- PyYAML

To install these libraries, run the following command:
pip install requests beautifulsoup4 pyyaml

Usage:
1. Save this script as a Python file (e.g., toc_extractor.py).
2. Run the script in the terminal or command prompt using Python:
   python toc_extractor.py
3. The TOC YAML files for each book will be created in the "data/book_info" directory.
"""


import os
import requests
from bs4 import BeautifulSoup
import yaml

def get_toc(url, book_code):
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception(f"Failed to fetch URL: {url}")

    soup = BeautifulSoup(response.content, "html.parser")
    toc = {}
    
    swedish_alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZÅÄÖ"
    
    if book_code == "sthlm45":
        anchor_names = {letter: letter for letter in swedish_alphabet}
    elif book_code == "norr68":
        anchor_names = {letter: f"n{letter.lower()}" for letter in swedish_alphabet}
    else:
        anchor_names = {letter: letter.lower() for letter in swedish_alphabet}
        anchor_names.update({"Å": "aa", "Ä": "ae", "Ö": "oe"})

    for letter in swedish_alphabet:
        letter_anchor_name = anchor_names[letter]
        letter_anchor = soup.find("a", {"name": letter_anchor_name})
        if letter_anchor:
            next_link = letter_anchor.find_next("a")
            if next_link and "href" in next_link.attrs:
                page_number = next_link["href"].split(".")[0]
                toc[letter] = int(page_number)
        else:
            print(f"No entries found for letter '{letter}'")

    return toc

directory = "data/"
os.makedirs(directory, exist_ok=True)

get_toc

toc_url = "http://runeberg.org/vemindu/"
toc_dict = get_toc(toc_url)
yaml_filename = os.path.join(directory, "vemindu_toc.yaml")

with open(yaml_filename, "w") as yaml_file:
    yaml.dump(toc_dict, yaml_file, default_flow_style=False)

print(f"YAML file created: {yaml_filename}")