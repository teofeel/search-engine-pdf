import json
import fitz
from entities.Trie import Trie
import re
from constants import PAGE_OFFSET
from entities import Graph


def pdf_to_hashmap():
    pdf_doc = fitz.open('Data Structures and Algorithms in Python.pdf')

    graph = Graph.Graph()
    for page_num in range(len(pdf_doc)):
        page = pdf_doc.load_page(page_num)
        page_text = page.get_text()

        page = Graph.PageNode(page_num+1, page_text, 0, Trie().insert_words_trie(page_text), min(page_num+2, len(pdf_doc)))
        
        graph.add_page(page)

        graph.add_edge(page_num+1, page.next_page)
        
    graph.dfs_create_page_links(1)
    return graph
 
        

def load_files():
    pass  

def save_files():
    pass
