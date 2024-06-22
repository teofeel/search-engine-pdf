import json
import fitz
from entities.Trie import Trie
import re

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
            'trie_structure': Trie().insert_words_trie(page_text)
        }
    
    return hashmap

def extract_page_links(text):

    pass

def load_files():
    pass  

def save_files():
    pass
