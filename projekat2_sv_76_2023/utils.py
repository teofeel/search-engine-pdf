import json
import fitz
from entities.Trie import Trie
import re
from constants import PAGE_OFFSET

def pdf_to_hashmap():
    pdf_doc = fitz.open('Data Structures and Algorithms in Python.pdf')

    hashmap = {}
    for page_num in range(len(pdf_doc)):
        page = pdf_doc.load_page(page_num)
        page_text = page.get_text()
        hashmap[page_num + 1] = {
            'content':page_text,
            'page_number':page_num + 1,
            'rang':0,
            'trie_structure': Trie().insert_words_trie(page_text),
            'page_connected': []
        }
    
    create_page_links(hashmap)

    return hashmap

def create_page_links(files):
    for file in files:
        text = files[file]['content']

        page_links = extract_page_link(text)

        for link in page_links:
            files[link+PAGE_OFFSET]['page_connected'].append(files[file]['page_number'])


def extract_page_link(text):
    patterns = [
        r'see page (\d+)',
        r'on page (\d+)',
        r'see pages (\d+) and (\d+)',
        r'on pages (\d+) and (\d+)',
        r'see page (\d+) and (\d+)'
    ]

    page_links = []
    for pattern in patterns:
        matches = re.findall(pattern, text, re.IGNORECASE)

        for match in matches:
            if(isinstance(match, tuple)):
                page_links.extend(match)
            else:
                page_links.append(match)

    try:
        return list(map(int, page_links))
    except:
        return []
    
        

def load_files():
    pass  

def save_files():
    pass
